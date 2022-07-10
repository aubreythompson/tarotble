from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin

import pandas as pd
import ast
from musixmatch import Musixmatch
import json
import os
from transformers import pipeline, set_seed

APIKEY = os.getenv('MUSIXMATCH_KEY')
url = 'https://api.musixmatch.com/ws/1.1/'
musixmatch = Musixmatch(APIKEY)

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/lyrics',methods=['GET'])
@cross_origin()
def lyrics():
    artist = request.args.get('artist')
    track = request.args.get('track')

    lyrics_dict = musixmatch.matcher_lyrics_get(q_track=track, q_artist=artist)

    if lyrics_dict['message']['header']['status_code']==200:
        lyrics = lyrics_dict['message']['body']['lyrics']['lyrics_body']
        print('lyrics', lyrics) # 53
        print('lyrics 60', lyrics[:60])
        prefix_text = '. Please reflect today on your life on your future on opportunity on beauty.'
        gens = generator(lyrics[:500] + prefix_text, max_length=1000, num_return_sequences=1, temperature=.8)
        print('gens', gens)
        return {'data': gens[0]['generated_text'][(500 + len(prefix_text)):]}, 200
    if lyrics_dict['message']['header']['status_code']==404:
        return {'message': "We couldn't find " + track + ' by ' + artist + ', sorry.'}, 404
    else:
        return {'message': "Please try again"}, 401

if __name__ == '__main__':
    app.run() 
