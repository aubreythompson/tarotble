from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)
from musixmatch import Musixmatch
import json
import os

#APIKEY = os.getenv('MUSIXMATCH_API_KEY')
APIKEY = '928dadc5c67821e645b1e38b6a414ddb'
url = 'https://api.musixmatch.com/ws/1.1/'
musixmatch = Musixmatch(APIKEY)

# from transformers import pipeline, set_seed

# generator = pipeline('text-generation', model='gpt2')

# set_seed(42)




@app.route('/lyrics',methods=['GET'])
def lyrics():
        
    # parser = reqparse.RequestParser()  # initialize
    # parser.add_argument('track', required=True)  # add arguments
    # parser.add_argument('artist', required=True)

    # args = parser.parse_args()  # parse arguments to dictionary

   
    artist = request.args.get('artist')
    track = request.args.get('track')
    # track = args['track']
    # artist = args['artist']

    lyrics_dict = musixmatch.matcher_lyrics_get(q_track=track, q_artist=artist)
  #  lyrics_dict = json.loads(lyrics_json)
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
        return {'message': "We couldn't find " + track + ' by ' + artist + ', sorry.'}, 401

#api.add_resource(Lyrics,'/lyrics')

if __name__ == '__main__':
    app.run() 
