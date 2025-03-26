from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.nn.functional import softmax
import json
import os

def classify_text(text):
    inputs = tokenizer(text, padding = True, truncation = True, max_length = 512, return_tensors = "pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = softmax(logits, dim = 1)
    labels = ['Negative', 'Neutral', 'Positive']
    predicted_label = labels[torch.argmax(probs)]
    return predicted_label, probs[0][0].item(), probs[0][2].item()

with open("json/news.json", "r", encoding = 'utf-8') as file:
    data = json.load(file)
    
file_path = "json/sentiment.json"
if not os.path.exists("json"):
    os.makedirs("json")

model_name = "ProsusAI/finbert"
model = BertForSequenceClassification.from_pretrained(model_name, num_labels = 3, ignore_mismatched_sizes = True)
tokenizer = BertTokenizer.from_pretrained(model_name)

sentiment_results = {}
for symbol in data:
    pos = neg = 0
    for news in data[symbol]:
        sentiment, neg_score, pos_score = classify_text(news)
        pos += pos_score
        neg += neg_score
    nss = round((pos - neg) / (pos + neg), 4)
    sentiment_results[symbol] = nss

with open(file_path, "w", encoding = 'utf-8') as file:
    json.dump(sentiment_results, file, indent = 4)

print("Net Sentiment Scores loaded!")
