from flask import Flask, request
import os
import utils
import requests
import json
from replit import db


app = Flask('app')

def get_transcripts():
  api_key = os.getenv('api_key')
  header = {
    'authorization': api_key,
    'content type': 'application/json'
  }

  audio_file = "real.mp3"
  upload_url = utils.upload_file(audio_file, header)

  transcript = utils.request_transcript(upload_url, header)

  print(transcript)

  polling_endpoint = utils.make_polling_endpoint(transcript)

  db['transcipt_url'] = polling_endpoint

  utils.wait_for_completion(polling_endpoint, header)

  paragraph = utils.get_paragraphs(polling_endpoint, header)

  audio_url = transcript['audio_url']
  db['audio_url'] = audio_url
  return paragraph

@app.route('/')
def hello_world():
  transcript = get_transcripts()
  return transcript['paragraphs'][0]['text']

app.run(host='0.0.0.0', port=8080)
