# from flask import Flask
# from flask_restful import Resource, Api, reqparse
# import pandas as pd
# import ast
# app = Flask(__name__)
# api = Api(app)
from musixmatch import Musixmatch

APIKEY = '928dadc5c67821e645b1e38b6a414ddb'
url = 'https://api.musixmatch.com/ws/1.1/'
musixmatch = Musixmatch(APIKEY)
lyrics = musixmatch.matcher_lyrics_get(q_track='need your love', q_artist='Tennis')

print(lyrics)