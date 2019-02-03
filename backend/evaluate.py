import torch
from torch.utils import data
import utils
import settings

if __name__ == "__main__":

    model = utils.simple_mlp
    model.load_state_dict(torch.load(settings.LOAD_MODEL))

    test_data = utils.BertEncodedSpamData('test')
    test_loader = data.DataLoader(test_data, batch_size=32, shuffle=False, num_workers=1)

    corrects = 0
    covered = 0

    for features, targets in test_loader:
        predictions = model(features)

        corrects += int((torch.round(predictions).long().view(-1) == targets).sum())
        covered += len(predictions)

        acc = corrects / covered

        print(f"Current accuracy: {acc}, corrects: {corrects}, covered: {covered} out of {len(test_data)}")
    print(f"Final accuracy: {corrects/covered}")


