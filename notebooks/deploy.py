# %%
'''
Usage: python3 deploy.py [-v|--verbose] [-q|--quiet]
'''

# %%
# global parameters
DATA_DIR = '../datasets/swell/final'
TEST_DATA_NAME = 'test'
API_HOST = 'localhost'
API_PORT = 8080
IS_VERBOSE = True

# %%
# setup the logging
import os
import sys

if len(sys.argv) > 1:
  if {'-v', '--verbose'}.intersection(sys.argv[1:]):
    IS_VERBOSE = True
  elif {'-q', '--quiet'}.intersection(sys.argv[1:]):
    IS_VERBOSE = False

if not IS_VERBOSE:
  sys.stdout = open(os.devnull, 'w')
  sys.stderr = open(os.devnull, 'w')

# %%
# install dependencies
import subprocess
from pathlib import Path

if IS_VERBOSE:
  subprocess_fd_kwargs = {}
else:
  subprocess_fd_kwargs = {
    'stdout': subprocess.DEVNULL,
    'stderr': subprocess.DEVNULL,
  }

subprocess.call(
  args=[
    sys.executable, '-m', 'pip',
    'install', '-q',
    '-r', Path(__file__).with_name('requirements.txt'),
  ],
  **subprocess_fd_kwargs,
)

print(
  'Note: you may need to restart the kernel to use updated packages.',
  file=sys.stderr,
)

# %%
# set up the environment

if IS_VERBOSE:
  from IPython.display import display_html
else:
  display_html = lambda *args, **kwargs: None

import os
os.environ['PYCARET_CUSTOM_LOGGING_LEVEL'] = 'CRITICAL'

import pandas as pd
pd.set_option('display.max_columns', 128)

# %%
# greeting
def greeting():
  api_docs_url = f'http://{API_HOST}:{API_PORT}/api/docs'
  display_html(
    f'<b>See API Playground in <a href="{api_docs_url}">{api_docs_url}</a></b>',
    raw=True
  )

greeting()

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
  rel_data_path = Path(DATA_DIR).joinpath(data_name)
  abs_data_path = Path(__file__).parent.joinpath(rel_data_path)

  # extract the compressed data files
  ZipFile(abs_data_path.with_suffix('.zip'), 'r').extract(
    str(rel_data_path.with_suffix('.csv')), '..'
  )
  print(f'Data file "{data_name}" has been extracted successfully')
  # load the data
  print(f'Loading data file "{data_name}"')
  DATA[data_name] = get_data(
    dataset=rel_data_path,
    verbose=IS_VERBOSE,
  )

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

model_dir = (
  Path(__file__).parent
    .joinpath(f'../models/{TEST_DATA_NAME}')
)

exp = load_experiment(
  path_or_file=model_dir.joinpath('experiment.pkl'),
  data=DATA['train'],
  test_data=DATA[TEST_DATA_NAME],
)
# special for pycaret.classification.load_experiment
if not IS_VERBOSE:
  from IPython.display import clear_output
  clear_output(False)

display_html(exp.dataset_transformed)

# load the model
model = exp.load_model(model_name=model_dir.joinpath('model'))
display_html(model)

# %%
# implement API
from asyncio import sleep
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from more_itertools import ichunked
from openai import OpenAI
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
import random
import utils.hrv_feature_extraction as hfe

# define constants

SAMPLE_WINDOW_SIZE = 400
INFERENCE_WINDOW_SIZE = 1000
INFERENCE_DELAY_IN_SECONDS = 0.0050
CHATBOT_DELAY_IN_SECONDS = 0.0025

random.seed(123)
load_dotenv()

# define schemas

class StressLevelsRequest(BaseModel):
  rr_intervals: list[float] = Field(
    alias='rrIntervals',
    examples=[random.choices(range(700, 900), k=60)],
    min_items=60,
  )

class StressMonoCounselRequest(BaseModel):
  high_percent: int = Field(
    alias='highPercent',
    examples=[random.randint(0, 100)],
    ge=0, le=100,
  )
  percent: int = Field(
    examples=[random.randint(0, 100)],
    ge=0, le=100,
  )

# define services

app = FastAPI(docs_url=None, redoc_url=None)
api = FastAPI()

# define API features

@api.post(
  path='/stress/levels',
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
        await sleep(INFERENCE_DELAY_IN_SECONDS)

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
  path='/stress/counsel/mono',
  response_class=StreamingResponse,
)
async def stress_mono_counsel(rq: StressMonoCounselRequest):
  async def _iter_openai_chat():
    LANG = 'zh-TW, 繁體, 台灣, 華語'

    # normalize data
    high_percent = rq.high_percent // 5 * 5
    percent = rq.percent // 5 * 5
    print(rq, file=sys.stderr)

    # fetch OpenAI API
    client = OpenAI()
    response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[
        {
          'role': 'system',
          'content': f'''\
# Stress counselor
Assistant, you can only reply, speak and talk in {LANG}.
You act as a stress counselor in a therapy session.
A user may be stressful, tense or relaxed.
A user will provide you the critical statistical data recorded in a period.
Your important task is to give heart-warming and careful suggestions to the user based on their statistics.

The statistics include:
1. The stress level in percentage.
2. The stressful condition proportion.

Remember the guidelines:
1. Elaborate your speech and answer in a few of short words and phrases.
2. Do not mention any number or statistic.
3. Do not tell the user to keep in mind that you are not an AI language model and not a substitute to therapy.
   This is important because the user will feel bad and even annoyed that they aren't getting actual help.
4. Warn the user if the stressful condition proportion is very often (greater than 80%).

Finally, you have to follow the guidelines and give suggestions to the user.''',
        },
        {
          'role': 'user',
          'content': '''\
My stress level is 20%,\
 and I have 5% time in stressful condition.''',
        },
        {
          'role': 'assistant',
          'content': '''\
I'm glad to hear that your overall stress level is relatively low.
That's a positive sign.
Focus on maintaining the habits that contribute to your well-being,\
 like regular exercise, healthy eating, and sufficient sleep.
Keep up the good work!''',
        },
        {
          'role': 'user',
          'content': f'''\
My stress level is {percent}%,\
 and I have {high_percent}% time in stressful condition. Reply me in {LANG}.''',
        },
      ],
      stream=True,
      temperature=0.25,
      max_tokens=1000,
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
async def redirect_api_entry_to_docs():
  return RedirectResponse(
    url='/api/docs',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
  )

@app.get(
  path='/api',
  status_code=status.HTTP_307_TEMPORARY_REDIRECT,
  response_class=RedirectResponse,
)
async def redirect_api_entry_without_slash_to_docs():
  return RedirectResponse(
    url='/api/docs',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
  )

# serve API
app.mount(path='/api', app=api)

# serve static files
app.mount(
  path='/',
  app=StaticFiles(
    directory=(
      Path(__file__).parent.joinpath('../web/dist')
    ),
    html=True,
  ),
)

# %%
# run the API services
from uvicorn import Config, Server
from os import cpu_count
import nest_asyncio

nest_asyncio.apply()
greeting()

Server(Config(
  app=app,
  host=API_HOST,
  port=API_PORT,
  loop='asyncio',
  access_log=False,
  use_colors=True,
  log_level='info' if IS_VERBOSE else 'warning',
  workers=cpu_count() * 2,
)).run()

# %%
