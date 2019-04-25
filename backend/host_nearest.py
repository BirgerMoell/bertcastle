import json

import torch
import flask
from flask import jsonify, request
from flask_cors import CORS

import nearest


app = flask.Flask(__name__)
CORS(app)

corpus = json.load(open('./data/movie_lines.json'))

ns = nearest.NearestSentence(corpus=corpus[:500])

#@app.route("/nearest/<path:text>")
#def nearest(text):
#    return ns.nearest(text)


@app.route('/nearest', methods=['POST'])
def classify():
      text = request.json['text']
      print(text)
      return jsonify(ns.nearest(text))
