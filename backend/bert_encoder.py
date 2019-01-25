import torch
import torch.nn as nn
import pytorch_pretrained_bert as bert

tokenizer = bert.BertTokenizer.from_pretrained('bert-base-uncased')
model = bert.BertModel.from_pretrained('bert-base-uncased')

# Step 1 Tokenize

class BertEncoder():
    def __init__(self):
        # Pytorch bert boilerplate
        self.tokenizer = bert.BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = bert.BertModel.from_pretrained('bert-base-uncased')
        self.model.eval()

    def tokenize(self, text, indexed):
        if (indexed):
            # Returns tokenized ids
            tokenized = self.tokenizer.tokenize(text)
            return self.tokenizer.convert_tokens_to_ids(tokenized)
        else:
            return self.tokenizer.tokenize(text)

    def get_word_from_token_id(self, id):
        tokens = self.tokenizer.convert_ids_to_tokens(id)
        return tokens

be = BertEncoder()
#print(be.tokenize("hello World is a SENTENCE", False))
print(be.tokenize("hello World is a SENTENCE", True))
print(be.tokenize("hello World in the world", True))
print(be.tokenize("this is the world of world", True))
print(be.tokenize("this is the world of world", True))

token_ids = be.tokenize("hello World is a SENTENCE", True)
tokens = be.get_word_from_token_id(range(6000,7000))

print(tokens)
# Convert inputs to PyTorch tensors
#tokens_tensor = torch.tensor([tokenized])
#print(tokens_tensor)

#x = 1

#print(tokenize("world hello", False))



# class BertWrapper():
#     def __init__(self):
#         # Pytorch bert boilerplate
#         self.tokenizer = bert.BertTokenizer.from_pretrained('bert-base-uncased')
#         self.model = bert.BertModel.from_pretrained('bert-base-uncased')
#         self.model.eval()

#     def encode(self, text):
#         tokenized_text = self.tokenizer.tokenize(text)
#         indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
#         segment_ids = [0 for i in indexed_tokens]  # Note, this can be improved

#         tokens = torch.tensor([indexed_tokens])
#         segments = torch.tensor([segment_ids])

#         _, features = self.model(tokens, segments)
#         return features.view(-1).detach()

#     def __call__(self, text):
#         return self.encode(text)


# simple_mlp = nn.Sequential(
#     nn.Linear(768, 128),
#     nn.ReLU(),
#     nn.Linear(128, 1),
#     nn.Sigmoid(),
# )

