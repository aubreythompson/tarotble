# from flask import Flask
# from flask_restful import Resource, Api, reqparse
# import pandas as pd
# import ast
# app = Flask(__name__)
# api = Api(app)
# from transformers import pipeline, set_seed

# generator = pipeline('text-generation', model='gpt2')

# set_seed(42)

# gens = generator("""I need your love and I need your touch""", max_length=200, num_return_sequences=5)

# for gen in gens:
#     print('gens', gen)

# print('length', len(gens))

from musixmatch import Musixmatch

APIKEY = '928dadc5c67821e645b1e38b6a414ddb'
url = 'https://api.musixmatch.com/ws/1.1/'
musixmatch = Musixmatch(APIKEY)
lyrics = musixmatch.matcher_lyrics_get(q_track='need your love', q_artist='Tennis')

print(lyrics)
