import torch
import flask
import utils

app = flask.Flask(__name__)

model = utils.simple_mlp
model.load_state_dict(torch.load("models/model9.params"))

bertwrap = utils.BertWrapper()

@app.route("/<path:text>")
def hello(text):
    features = bertwrap(text)
    out = model(features.view(1, -1))
    val = float(out)

    return f"{val}"
