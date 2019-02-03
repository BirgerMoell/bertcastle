import json
import utils
import settings

import tqdm
import torch
import collections

import sklearn.cluster as cluster

import numpy as np


class NearestSentence:

    def __init__(self,*, corpus: tuple):
        """
        Splits the corpus into sentences, and maps these into some latent space.
        """
        self.n_clusters = len(corpus) // 500

        self.bert = utils.BertWrapper(bert_path=settings.BERT_PATH, vocab=settings.VOCAB)
        self.corpus = corpus
        self.kmeans = cluster.KMeans(n_clusters=self.n_clusters)

        print("Sentences")
        print(len(self.corpus))

        self.codes = []
        for sentence in tqdm.tqdm(self.corpus):
            self.codes.append(self.bert(sentence))
        self.codes = tuple(self.codes)

        # Do K-means
        np_codes = np.stack(map(lambda i: i.numpy(), self.codes))
        cluster_indices = self.kmeans.fit_predict(np_codes)

        # Map clusters
        self.clusters = collections.defaultdict(list)

        for i in range(len(self.corpus)):
            self.clusters[cluster_indices[i]].append((self.corpus[i], self.codes[i]))

        print('NearestSentence ready')

    def nearest(self, sentence: str):
        code = self.bert(sentence)
        cluster_idx = int(self.kmeans.predict(code.numpy().reshape(1, -1)))

        m = 1e3
        s = 'Derp'
        for line, code2 in self.clusters[cluster_idx]:
            distance = torch.sqrt(torch.mean((code2 - code) ** 2))
            if distance < m:
                m = distance
                s = line

        return s
        

if __name__=="__main__":

    corpus = tuple(json.load(open('./data/movie_lines.json')))
    corpus_short = corpus[:1000]
    ns = NearestSentence(corpus=corpus_short)

    print(ns.nearest('Yo'))


