import numpy as np
import pandas as pd
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

urls = pd.read_csv('dataset.csv')

# print(type(urls))

print(urls.head())


def make_tokens(f):
    tokens_by_slash = str(f.encode('utf-8')).split('/')
    total_tokens = []
    for i in tokens_by_slash:
        tokens = str(i).split('-')
        tokens_by_dot = []
        for j in range(0, len(tokens)):
            temp_tokens = str(tokens[j]).split('.')
            tokens_by_dot += temp_tokens
        total_tokens += tokens + tokens_by_dot
    total_tokens = list(set(total_tokens))
    if 'com' in total_tokens:
        total_tokens.remove('com')
    return total_tokens


y = urls['label']
# print(y)
url_list = urls['url']

vectorizer = TfidfVectorizer(tokenizer=make_tokens)
x = vectorizer.fit_transform(url_list)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

logit = LogisticRegression()
logit.fit(x_train, y_train)

print('Accuracy : ', logit.score(x_test, y_test))

