# %%
# global parameters
DATA_DIR = '../datasets/swell/final'
TEST_DATA_NAME = 'test-custom-1'
API_HOST = 'localhost'
API_PORT = 8081

# %%
from IPython.display import display_html

def greeting():
  api_playground_url = f'http://{API_HOST}:{API_PORT}/api/playground'
  display_html(
    f'<b>See API Playground in <a href="{api_playground_url}">{api_playground_url}</a></b>',
    raw=True
  )

greeting()

# %%
# set up the environment
import os
os.environ['PYCARET_CUSTOM_LOGGING_LEVEL'] = 'CRITICAL'

import pandas as pd
pd.set_option('display.max_columns', 128)

# %%
# prepare the data
from pathlib import Path
from pycaret.datasets import get_data
from zipfile import ZipFile

DATA = {
  name: None
  for name in ['train', TEST_DATA_NAME]
}

for data_name in DATA.keys():
  data_path = Path(DATA_DIR).joinpath(data_name)
  # extract the compressed data files
  ZipFile(data_path.with_suffix('.zip'), 'r').extract(
    str(data_path.with_suffix('.csv')), '..'
  )
  print(f'Data file "{data_name}" has been extracted successfully')
  # load the data
  print(f'Loading data file "{data_name}"')
  DATA[data_name] = get_data(dataset=f'{data_path}')

# %%
# custom target encoding
for data_name in DATA.keys():
  data = DATA[data_name]
  data['condition'] = data['condition'].map({
    'no stress': 0,
    'interruption': 1,
    'time pressure': 2,
  })

# %%
# load the experiment and the model
from pathlib import Path
from pycaret.classification import load_experiment

model_dir = Path(f'../models/{TEST_DATA_NAME}')

exp = load_experiment(
  path_or_file=model_dir.joinpath('experiment.pkl'),
  data=DATA['train'],
  test_data=DATA[TEST_DATA_NAME],
)
from IPython.display import display_html
display_html(exp.dataset_transformed.head(5))

# load the model
model = exp.load_model(model_name=model_dir.joinpath('model'))
display_html(model)

# %%
# implement API
from asyncio import sleep
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, StreamingResponse
from more_itertools import ichunked
from openai import OpenAI
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
import random
import utils.hrv_feature_extraction as hfe

# define constants

SAMPLE_WINDOW_SIZE = 400
INFERENCE_WINDOW_SIZE = 250
INFER_DELAY_IN_SECONDS = 0.005
CHATBOT_DELAY_IN_SECONDS = 0.05
random.seed(123)
load_dotenv()

# define schemas

class StressLevelsRequest(BaseModel):
  rr_intervals: list[float] = Field(
    examples=[random.choices(range(700, 900), k=60)],
    min_items=60,
  )

class StressMonoConsultRequest(BaseModel):
  percent: int = Field(
    examples=[random.randint(0, 100)],
    ge=0, le=100,
  )

# define features

api = FastAPI(
  docs_url='/api/playground',
  redoc_url='/api/docs',
  openapi_url='/api/openapi.json',
  swagger_ui_oauth2_redirect_url='/api/playground/oauth2-redirect',
)

@api.post(
  path=f'/api/stress/levels',
  response_class=StreamingResponse,
)
async def stress_levels(rq: StressLevelsRequest):
  def _iter_features(iterable):
    for window in hfe.get_window_iterator(
      values=iterable,
      window_size=SAMPLE_WINDOW_SIZE,
    ):
      yield hfe.extract_hrv_features_from_rri_window(
        rri_window=window,
      )

  async def _iter_levels(iterable):
    for features in ichunked(
      _iter_features(iterable),
      INFERENCE_WINDOW_SIZE,
    ):
      for _, row in exp.predict_model(
        estimator=model,
        data=pd.DataFrame(features),
        verbose=False,
        raw_score=True,
      ).iterrows():
        weighted_level = (
          row['prediction_score_0'] * 0 +
          row['prediction_score_1'] * 1 +
          row['prediction_score_2'] * 2
        )
        yield f'{weighted_level:.4f}\n'
        await sleep(INFER_DELAY_IN_SECONDS)

  rr_intervals = np.array(rq.rr_intervals)

  return StreamingResponse(
    content=_iter_levels(rr_intervals),
    headers={
      'X-Stream-Length': str(
        1 + max(0, len(rr_intervals) - SAMPLE_WINDOW_SIZE)
      ),
    },
    media_type='text/plain',
  )

@api.post(
  path=f'/api/stress/consult/mono',
  response_class=StreamingResponse,
)
async def stress_mono_consult(rq: StressMonoConsultRequest):
  async def _iter_openai_chat():
    client = OpenAI()
    response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[
        {
          'role': 'system',
          'content': 'Greeting bot, says Hi with the number.',
        },
        {
          'role': 'user',
          'content': f'Hello? I am number {rq.percent}.',
        },
      ],
      stream=True,
    )
    for chunk in response:
      message = chunk.choices[0].delta.content
      if message:
        yield message
        await sleep(CHATBOT_DELAY_IN_SECONDS)

  return StreamingResponse(
    content=_iter_openai_chat(),
    media_type='text/plain',
  )

@api.get(
  path='/',
  status_code=status.HTTP_307_TEMPORARY_REDIRECT,
  response_class=RedirectResponse,
)
async def entry():
  # temporary redirect to API Playground
  return RedirectResponse(
    url='/api/playground',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
  )

# %%
# run the API services
from uvicorn import Config, Server
from os import cpu_count

# start the serving loop
greeting()
Server(Config(
  app=api,
  host=API_HOST,
  port=API_PORT,
  loop='asyncio',
  access_log=False,
  # log_level='debug',
  use_colors=True,
  workers=cpu_count() * 2,
)).run()

# %%
# clean up
exit(0)

