# define the feature extraction method
from numpy.typing import NDArray
from pandas._typing import ArrayLike
from typing import Iterable

def get_window_iterator(
  values: ArrayLike,
  window_size: int,
) -> Iterable[ArrayLike]:
  '''
  Iterate over windows of data from an array-like object.

  ### Parameters:
  - values: An array-like object.
  - window_size: The window size.

  ### Returns:
  - An iterator over windows of array-like object.
  '''
  window_end = len(values)
  window_size = int(window_size)
  if window_size < window_end:
    for index in range(window_end + 1 - window_size):
      yield values[index: index + window_size]
  else:
    yield values

def extract_hrv_features_from_rri_window(
  rri_window: NDArray,
) -> dict[str, float]:
  '''
  Extracts HRV features from a window of RR intervals.

  ### Parameters:
  - rri_window: A window of RR intervals in milliseconds.
  - fs: The sampling frequency in Hz.

  ### Returns:
  - A mapping that contains HRV features.

  ### References:
  - Nkurikiyeyezu, Kizito & Shoji, Kana & Yokokubo, Anna & Lopez, Guillaume. (2019). Thermal Comfort and Stress Recognition in Office Environment. 10.5220/0007368802560263.
  '''
  from antropy import sample_entropy, higuchi_fd
  import numpy as np
  from scipy.interpolate import interp1d
  from scipy.stats import skew, kurtosis
  from scipy.signal import welch

  rri_window = np.array(rri_window)
  ws = len(rri_window) # sample size

  mrr = np.mean(rri_window)
  sdrr = np.std(rri_window)
  sd = np.diff(rri_window)
  sdsd = np.std(sd)
  rmssd = np.mean(sd ** 2) ** 0.5
  asd = abs(sd)

  rel_rr = sd / (rri_window[1:] + rri_window[:-1]) * 2
  rel_sd = np.diff(rel_rr)
  rel_sdrr = np.std(rel_rr)
  rel_rmssd = np.mean(rel_sd ** 2) ** 0.5

  int_rr_x = np.cumsum(rri_window) / 1000
  int_rr_x_new = np.arange(1, max(int_rr_x))
  int_rr = interp1d(
    x=int_rr_x, y=rri_window, copy=False,
    kind='cubic', fill_value='extrapolate',
  )(int_rr_x_new)
  F, P = welch(x=int_rr, nperseg=min(ws, len(int_rr_x_new)))
  cond_vlf = (F >= 0.003) & (F <= 0.04)
  cond_lf = (F >= 0.04) & (F <= 0.15)
  cond_hf = (F >= 0.15) & (F <= 0.4)
  vlf = np.trapz(y=P[cond_vlf], x=F[cond_vlf])
  lf = np.trapz(y=P[cond_lf], x=F[cond_lf])
  hf = np.trapz(y=P[cond_hf], x=F[cond_hf])
  nu = lf + hf
  tp = vlf + nu

  return {
    'MEAN_RR': mrr,
    'MEDIAN_RR': np.median(rri_window),
    'SDRR': sdrr,
    'RMSSD': rmssd,
    'SDSD': sdsd,
    'SDRR_RMSSD': sdrr / rmssd,
    'HR': 60000 / mrr,
    'pNN25': np.mean(asd > 25) * 100,
    'pNN50': np.mean(asd > 50) * 100,
    'KURT': kurtosis(rri_window),
    'SKEW': skew(rri_window),
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
    'sampen': sample_entropy(x=rri_window, order=0),
    'higuci': higuchi_fd(rri_window),
    'datasetId': 2,
  }
