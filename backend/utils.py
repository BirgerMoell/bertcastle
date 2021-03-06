import os
import tempfile
import tqdm
import pickle

import torch
from torch.utils import data
import torch.nn as nn
import pandas as pd

import pytorch_pretrained_bert as bert


class BertWrapper():

    def __init__(self,*, bert_path: "Path to stored offline bert model" = None, vocab = None):

        if vocab:
            self.tokenizer = bert.BertTokenizer.from_pretrained(vocab)
        else:
            self.tokenizer = bert.BertTokenizer.from_pretrained('bert-base-uncased')

        if bert_path:
            self.model = torch.load(bert_path)
        else:
            # This will fetch a remotely hosted model and does not work offline
            self.model = bert.BertModel.from_pretrained('bert-base-uncased')

        self.model.eval()

    def encode(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segment_ids = [0 for i in indexed_tokens]  # Note, this can be improved

        tokens = torch.tensor([indexed_tokens])
        segments = torch.tensor([segment_ids])

        _, features = self.model(tokens, segments)
        return features.view(-1).detach()

    def __call__(self, text):
        return self.encode(text)


class BertEncodedSpamData(data.Dataset):
    def __init__(self, mode,*, bert_path=None):
        super().__init__()
        self.df = pd.read_csv("./data/spam.csv")

        point = int((len(self.df)*0.7))
        self.df = self.df[:point] if mode == "train" else self.df[point:]

        self.start_idx = 0 if mode == "train" else point

        self.bertwrapper = BertWrapper(bert_path=bert_path)


    def __getitem__(self, item):
        item += self.start_idx
        label, text = tuple(self.df[key][item] for key in ("v1", "v2"))

        label_ohe = 1 if label == "spam" else 0  # It's very nice

        bert_text = self.bertwrapper.encode(text)

        return bert_text, torch.tensor(label_ohe)

    def __len__(self):
        return len(self.df)


def daze(dataset: "instance of a dataset", verbose=False):
    """ Stores the entire dataset on disk and returns a
    dazed version of the dataset """

    get_path = lambda i: os.path.join(tempfile.gettempdir(), f"{i}.pickle")

    class DazedData(dataset.__class__):
        def __init__(self, dataset):
            self.len = len(dataset)

        def __getitem__(self, item):
            if item not in range(self.len):
                raise IndexError("Index out of range")
            return pickle.load(open(get_path(item), "rb"))

        def __len__(self):
            return self.len

    progress = tqdm.tqdm if verbose else lambda i: i

    for item in progress(range(len(dataset))):
        pickle.dump(dataset[item], open(get_path(item), "wb"))

    return DazedData(dataset)


simple_mlp = nn.Sequential(
    nn.Linear(768, 128),
    nn.ReLU(),
    nn.Linear(128, 1),
    nn.Sigmoid(),
)

