# define the feature extraction method
from numpy import ndarray
from pandas import DataFrame
from typing import Iterable

def extract_hrv_features_from_rri(
  rr: Iterable[float],
  fs = 4,
  ws = 300,
) -> DataFrame:
  '''
  Extracts HRV features from a series of RR intervals.

  ### Parameters:
  - rr (Iterable[float]): A series of RR intervals in milliseconds.
  - fs (int): The sampling frequency in Hz.
  - ws (int): The window size in seconds.

  ### Returns:
  - DataFrame: A DataFrame that contains a series of HRV features.
  '''

  return DataFrame(_extract_hrv_features_from_rri(
    rr=rr, fs=fs, ws=ws,
  ))

def extract_hrv_features_from_labelled_rri(
  data: DataFrame,
  fs = 4,
  ws = 300,
) -> DataFrame:
  '''
  Extracts HRV features from dataset. (`DataFrame {label, rri}`)

  ### Parameters:
  - data (DataFrame):
    A dict-like object with series of `label` and `rri` data.
    RR intervals are in milliseconds.
  - fs (int): The sampling frequency in Hz.
  - ws (int): The window size in seconds.
  '''
  return DataFrame(_extract_hrv_features_from_labelled_rri(
    data=data,
    fs=fs,
    ws=ws,
  ))

def _extract_hrv_features_from_rri(
  rr: Iterable[float],
  fs: float,
  ws: float,
) -> Iterable[dict[str, float]]:
  import numpy as np

  rr = np.array(rr)
  ss = fs * ws # sample size

  for rr_win_end in np.arange(ss, len(rr) + 1):
    yield _extract_hrv_features_from_rri_window(
      rr_win=rr[rr_win_end-ss: rr_win_end],
      fs=fs,
      ws=ws,
    )

def _extract_hrv_features_from_labelled_rri(
  data: DataFrame,
  fs: float,
  ws: float,
) -> Iterable[dict[str, float]]:
  import numpy as np

  ss = fs * ws # sample size

  for data_win_end in np.arange(ss, len(data) + 1):
    data_win = data[data_win_end-ss: data_win_end]
    features = _extract_hrv_features_from_rri_window(
      rr_win=data_win['rri'].values,
      fs=fs,
      ws=ws,
    )
    features['condition'] = data_win['label'].value_counts().idxmax()
    yield features


def _extract_hrv_features_from_rri_window(
  rr_win: ndarray[float],
  fs: float,
  ws: float,
) -> dict[str, float]:
  from antropy import sample_entropy, higuchi_fd
  import numpy as np
  from scipy.interpolate import interp1d
  from scipy.stats import skew, kurtosis
  from scipy.signal import welch

  mrr = np.mean(rr_win)
  sdrr = np.std(rr_win)
  sd = np.diff(rr_win)
  sdsd = np.std(sd)
  rmssd = np.mean(sd ** 2) ** 0.5
  asd = abs(sd)

  rel_rr = sd / (rr_win[1:] + rr_win[:-1]) * 2
  rel_sd = np.diff(rel_rr)
  rel_sdrr = np.std(rel_rr)
  rel_rmssd = np.mean(rel_sd ** 2) ** 0.5

  int_rr_x = np.cumsum(rr_win) / 1000
  int_rr_x_new = np.arange(1, max(int_rr_x), 1 / fs)
  int_rr = interp1d(
    x=int_rr_x, y=rr_win, copy=False,
    kind='cubic', fill_value='extrapolate',
  )(int_rr_x_new)
  fr, ps = welch(
    x=int_rr, fs=fs,
    nperseg=min(ws * fs, len(int_rr_x_new)),
  )
  cond_vlf = (fr >= 0.003) & (fr <= 0.04)
  cond_lf = (fr >= 0.04) & (fr <= 0.15)
  cond_hf = (fr >= 0.15) & (fr <= 0.4)
  vlf = np.trapz(y=ps[cond_vlf], x=fr[cond_vlf])
  lf = np.trapz(y=ps[cond_lf], x=fr[cond_lf])
  hf = np.trapz(y=ps[cond_hf], x=fr[cond_hf])
  nu = lf + hf
  tp = vlf + nu

  return {
    'MEAN_RR': mrr,
    'MEDIAN_RR': np.median(rr_win),
    'SDRR': sdrr,
    'RMSSD': rmssd,
    'SDSD': sdsd,
    'SDRR_RMSSD': sdrr / rmssd,
    'HR': 60000 / mrr,
    'pNN25': np.mean(asd > 25) * 100,
    'pNN50': np.mean(asd > 50) * 100,
    'KURT': kurtosis(rr_win),
    'SKEW': skew(rr_win),
    'SD1': (2 ** -0.5) * sdsd,
    'SD2': (2 * (sdrr ** 2) - 0.5 * (sdsd ** 2)) ** 0.5,
    'MEAN_REL_RR': np.mean(rel_rr),
    'MEDIAN_REL_RR': np.median(rel_rr),
    'SDRR_REL_RR': rel_sdrr,
    'RMSSD_REL_RR': rel_rmssd,
    'SDSD_REL_RR': np.std(rel_sd),
    'SDRR_RMSSD_REL_RR': rel_sdrr / rel_rmssd,
    'KURT_REL_RR': kurtosis(rel_rr),
    'SKEW_REL_RR': skew(rel_rr),
    'VLF': vlf,
    'VLF_PCT': vlf / tp * 100,
    'LF': lf,
    'LF_PCT': lf / tp * 100,
    'LF_NU': lf / nu * 100,
    'HF': hf,
    'HF_PCT': hf / tp * 100,
    'HF_NU': hf / nu * 100,
    'TP': tp,
    'LF_HF': lf / hf,
    'HF_LF': hf / lf,
    'sampen': sample_entropy(x=rr_win, order=0),
    'higuci': higuchi_fd(rr_win),
    'datasetId': 2,
  }
