import tqdm

import torch
import torch.nn as nn

import torch.utils.data as data
import pytorch_pretrained_bert as bert

import pandas as pd


class BertEncodedSpamData(data.Dataset):
    def __init__(self, mode):
        super().__init__()
        self.df = pd.read_csv("./data/spam.csv")

        point = int((len(self.df)*0.7))
        self.df = self.df[:point] if mode == "train" else self.df[point:]

        # Pytorch bert boilerplate
        self.tokenizer = bert.BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = bert.BertModel.from_pretrained('bert-base-uncased')
        self.model.eval()

    def _encode(self, text):
        tokenized_text = self.tokenizer.tokenize(text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segment_ids = [0 for i in indexed_tokens]  # Note, this can be improved

        tokens = torch.tensor([indexed_tokens])
        segments = torch.tensor([segment_ids])

        _, features = self.model(tokens, segments)
        return features.view(-1).detach()

    def __getitem__(self, item):
        label, text = tuple(self.df[key][item] for key in ("v1", "v2"))

        label_ohe = 1 if label == "spam" else 0  # It's very nice

        bert_text = self._encode(text)

        return bert_text, torch.tensor(label_ohe)

    def __len__(self):
        return len(self.df)


def train(model, data_loader, epochs):
    pass


if __name__=="__main__":

    model = nn.Sequential(
        nn.Linear(768, 128),
        nn.ReLU(),
        nn.Linear(128, 1),
        nn.Sigmoid(),
    )

    train_data = BertEncodedSpamData('train')
    test_data = BertEncodedSpamData('test')

    train_loader = data.DataLoader(train_data, batch_size=32, shuffle=True, num_workers=1)
    test_loader = data.DataLoader(test_data, batch_size=32, shuffle=False, num_workers=1)

    criterion = nn.BCELoss()

    optimizer = torch.optim.Adam(model.parameters())

    # Main train loop
    epochs = 5
    for epoch in range(epochs):
        for features, targets in tqdm.tqdm(train_loader):
            predictions = model(features)
            loss = criterion(predictions, targets.float())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        torch.save(model.state_dict(), f'models/model{epoch}.params')
        print(loss)


