import tqdm
import torch
import torch.nn as nn
import torch.utils.data as data
import pandas as pd
import utils
import settings


def train(*, model, data_loader, epochs=100, save=True):

    criterion = nn.BCELoss()

    for epoch in range(epochs):

        for features, targets in tqdm.tqdm(data_loader):

            predictions = model(features)
            loss = criterion(predictions, targets.float())

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if save:
            torch.save(model.state_dict(), f'models/model{epoch}.params')
        print(loss)


if __name__=="__main__":

    model = utils.simple_mlp

    train_data = utils.daze(
        utils.BertEncodedSpamData('train', bert_path=settings.BERT_PATH),
        verbose=True)

    train_loader = data.DataLoader(train_data, batch_size=32, shuffle=True, num_workers=1)

    optimizer = torch.optim.Adam(model.parameters())

    # Main train loop
    train(model=model, data_loader=train_loader, epochs=100, save=True)

