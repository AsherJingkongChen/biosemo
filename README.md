# Fear detection experiments

## Datasets

### ECG Spider Clip
> Electrocardiogram, skin conductance and respiration from spider-fearful individuals watching spider video clips
- source [link](https://physionet.org/content/ecg-spider-clip/)
- citations
```plaintext
Ihmig, F. R., Gogeascoechea, A., Schäfer, S., Lass-Hennemann, J., & Michael, T. (2020). Electrocardiogram, skin conductance and respiration from spider-fearful individuals watching spider video clips (version 1.0.0). PhysioNet. https://doi.org/10.13026/sq6q-zg04.
```

### SWELL (Kaggle)
> This dataset comprises of heart rate variability (HRV) indices computed from the multimodal SWELL knowledge work (SWELL-KW) dataset for research on stress and user modeling (see. [http://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html](http://cs.ru.nl/~skoldijk/SWELL-KW/Dataset.html)).
- source:
  - [link 1](https://www.kaggle.com/datasets/qiriro/swell-heart-rate-variability-hrv/)
  - [link 2](https://www.kaggle.com/datasets/qiriro/stress/)
  - [link 3](https://arxiv.org/pdf/1910.01770.pdf)
  - [link 4](https://www.researchgate.net/publication/330754493_Thermal_Comfort_and_Stress_Recognition_in_Office_Environment)
- citations
```plaintext
1. S. Koldijk, M. A. Neerincx, and W. Kraaij, “Detecting Work Stress in Offices by Combining Unobtrusive Sensors,” IEEE Trans. Affect. Comput., vol. 9, no. 2, pp. 227–239, 2018.
2. S. Koldijk, M. Sappelli, S. Verberne, M. A. Neerincx, and W. Kraaij, “The SWELL Knowledge Work Dataset for Stress and User Modeling Research,” Proc. 16th Int. Conf. Multimodal Interact. - ICMI ’14, pp. 291–298, 2014.
3. Kraaij, Prof.dr.ir. W. (Radboud University & TNO); Koldijk, MSc. S. (TNO & Radboud University); Sappelli, MSc M. (TNO & Radboud University) (2014): The SWELL Knowledge Work Dataset for Stress and User Modeling Research. DANS. https://doi.org/10.17026/dans-x55-69zp
```

## Other References

### Heart Rate Variability Metrics and Norms
- source [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5624990/)

## Workflow

### Notebooks
Run them in this order for fully reproducing the experiment:
1. `src/preprocess.ipynb`
2. `src/analyze.ipynb`
3. `src/deploy.ipynb`
