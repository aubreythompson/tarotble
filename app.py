from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)
from musixmatch import Musixmatch
import json

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
        # gens = generator("""I need your love and I need your touch""", max_length=50, num_return_sequences=1)
        # print('length', len(gens))
        return {'data': lyrics}, 200
    else:
        return {'message': "We couldn't find " + track + ' by ' + artist + ', sorry.'}, 401

#api.add_resource(Lyrics,'/lyrics')

if __name__ == '__main__':
    app.run() 