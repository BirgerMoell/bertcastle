import tqdm

import torch
import torch.nn as nn

import torch.utils.data as data

import pandas as pd

import utils


def train(model, data_loader, epochs):
    pass


if __name__=="__main__":

    model = utils.simple_mlp

    train_data = utils.daze(utils.BertEncodedSpamData('train'), verbose=True)

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


