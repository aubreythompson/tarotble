from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
from musixmatch import Musixmatch
import json
import os

from aitextgen import aitextgen
# With your trained model, you can reload the model at any time by
# providing the folder containing the pytorch_model.bin model weights + the config, and providing the tokenizer.
ai2 = aitextgen(model_folder="trained_model",
               tokenizer_file="aitextgen.tokenizer.json")


#APIKEY = os.getenv('MUSIXMATCH_API_KEY')
APIKEY = '928dadc5c67821e645b1e38b6a414ddb'
url = 'https://api.musixmatch.com/ws/1.1/'
musixmatch = Musixmatch(APIKEY)

@app.route('/lyrics',methods=['GET'])
def lyrics():
   
    artist = request.args.get('artist')
    track = request.args.get('track')
 
    lyrics_dict = musixmatch.matcher_lyrics_get(q_track=track, q_artist=artist)
    if lyrics_dict['message']['header']['status_code']==200:
        lyrics = lyrics_dict['message']['body']['lyrics']['lyrics_body']

        lines = lyrics.split("\n")
        no_lyrics_resp = ''
        for line in lines[:5]:
            gentext = ai2.generate_one(prompt=line+"\n")
            no_lyrics = gentext.split("\n")[1]
            #print(no_lyrics)
            no_lyrics_resp = no_lyrics_resp + no_lyrics + "\n" 
        return {'data': no_lyrics_resp}, 200
    if lyrics_dict['message']['header']['status_code']==404:
        return {'message': "We couldn't find " + track + ' by ' + artist + ', sorry.'}, 404
    else:
        return {'message': "We couldn't find " + track + ' by ' + artist + ', sorry.'}, 401

if __name__ == '__main__':
    app.run() 
