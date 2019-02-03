import os

# Path to local bert model
BERT_PATH = None #os.path.expanduser('~/Data/Models/bert-base-uncased.model')

# Path to trained baseline model for serving or evaluation (spam classification)
LOAD_MODEL = None

# Either a string such as 'bert-base-uncased' or a path to a vocabulary file for BertTokenizer
VOCAB = None #os.path.expanduser("~/Data/Models/bert-base-uncased-vocab.txt")
