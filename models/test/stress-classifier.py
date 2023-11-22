# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("../models/test/stress-classifier")

# Create input/output pydantic models
input_model = create_model("../models/test/stress-classifier_input", **{'MEAN_RR': 885.1578369140625, 'MEDIAN_RR': 853.7637329101562, 'SDRR': 140.97274780273438, 'RMSSD': 15.55450439453125, 'SDSD': 15.55337142944336, 'SDRR_RMSSD': 9.063145637512207, 'HR': 69.49995422363281, 'pNN25': 11.133333206176758, 'pNN50': 0.5333333611488342, 'SD1': 11.001564979553223, 'SD2': 199.06178283691406, 'KURT': -0.8565537929534912, 'SKEW': 0.33521798253059387, 'MEAN_REL_RR': -0.00020298591698519886, 'MEDIAN_REL_RR': -0.00017922272672876716, 'SDRR_REL_RR': 0.017079949378967285, 'RMSSD_REL_RR': 0.007968840189278126, 'SDSD_REL_RR': 0.007968837395310402, 'SDRR_RMSSD_REL_RR': 2.1433420181274414, 'KURT_REL_RR': -0.8565537929534912, 'SKEW_REL_RR': 0.33521798253059387, 'VLF': 2661.89404296875, 'VLF_PCT': 72.20328521728516, 'LF': 1009.2493896484375, 'LF_PCT': 27.37566566467285, 'LF_NU': 98.48526000976562, 'HF': 15.522602081298828, 'HF_PCT': 0.4210471510887146, 'HF_NU': 1.5147371292114258, 'TP': 3686.666259765625, 'LF_HF': 65.01805114746094, 'HF_LF': 0.015380343422293663, 'sampen': 2.139754056930542, 'higuci': 1.1634851694107056})
output_model = create_model("../models/test/stress-classifier_output", prediction='no stress')


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8081)
