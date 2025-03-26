from yahoo_fin import news
import json
import os

json_file_path = "json"
if not os.path.exists(json_file_path):
    os.makedirs(json_file_path)

symbol_file = f"{json_file_path}/symbols.json"
with open(symbol_file, 'r', encoding = 'utf-8') as file:
    data = json.load(file)

symbols = data.get('ticker', [])
if not symbols:
    print('No Symbols')
    exit()

all_news = {}
for one_symbol in symbols:
    articles = news.get_yf_rss(one_symbol)
    for article in articles:
        if one_symbol not in all_news:
            all_news[one_symbol] = [article['summary']]
        else:
            all_news[one_symbol].append(article['summary'])
    print(f"{one_symbol}_news added to the file!")

output_file = f"{json_file_path}/news.json"
with open(output_file, 'w', encoding = 'utf-8') as file:
    json.dump(all_news, file, indent = 4)