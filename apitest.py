import requests
import json
from openai import Openai

with open('config.json') as f:
    config = json.load(f)
OAIapi_key = config['openAIKey']


openai.api_key = OAIapi_key

client.embeddings.create(
  model="text-embedding-3-large	",
  input="The food was delicious and the waiter...",
  encoding_format="float"
)