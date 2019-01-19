import tqdm
import torch
import torch.nn as nn
import torch.utils.data as data
import pandas as pd
import utils

class BertEncodedSpamData(data.Dataset):
    def __init__(self, mode):
        super().__init__()
        self.df = pd.read_csv("./data/spam.csv")

        point = int((len(self.df)*0.7))
        self.df = self.df[:point] if mode == "train" else self.df[point:]

        self.bertwrapper = utils.BertWrapper()


    def __getitem__(self, item):
        label, text = tuple(self.df[key][item] for key in ("v1", "v2"))

        label_ohe = 1 if label == "spam" else 0  # It's very nice

        bert_text = self.bertwrapper.encode(text)

        return bert_text, torch.tensor(label_ohe)

    def __len__(self):
        return len(self.df)


def train(model, data_loader, epochs):
    pass


if __name__=="__main__":

    model = utils.simple_mlp

    train_data = utils.daze(BertEncodedSpamData('train'), verbose=True)
    test_data = BertEncodedSpamData('test')

    train_loader = data.DataLoader(train_data, batch_size=32, shuffle=True, num_workers=1)
    test_loader = data.DataLoader(test_data, batch_size=32, shuffle=False, num_workers=1)

    criterion = nn.BCELoss()

    optimizer = torch.optim.Adam(model.parameters())

    # Main train loop
    epochs = 100
    for epoch in range(epochs):
        for features, targets in tqdm.tqdm(train_loader):
            predictions = model(features)
            loss = criterion(predictions, targets.float())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        torch.save(model.state_dict(), f'models/model{epoch}.params')
        print(loss)


