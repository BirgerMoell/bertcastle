import json

import torch
import flask
from flask import jsonify, request
from flask_cors import CORS

import nearest


app = flask.Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

corpus = json.load(open('./data/movie_lines.json'))

ns = nearest.NearestSentence(corpus=corpus[:600])

@app.route("/nearest/<path:text>")
def nearest(text):
    return ns.nearest(text)

