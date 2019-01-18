import torch
import torch.nn as nn

import pytorch_pretrained_bert as bert


class BertWrapper():
    def __init__(self):
        # Pytorch bert boilerplate
        self.tokenizer = bert.BertTokenizer.from_pretrained('bert-base-uncased')
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


simple_mlp = nn.Sequential(
    nn.Linear(768, 128),
    nn.ReLU(),
    nn.Linear(128, 1),
    nn.Sigmoid(),
)

