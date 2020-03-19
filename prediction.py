import numpy as np
import pandas as pd
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

urls = pd.read_csv('dataset.csv')

# print(type(urls))

print(urls.head())