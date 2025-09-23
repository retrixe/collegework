"""AIESL Assignment 6: NLP"""


import random
import math
import warnings
from newspaper import Article
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

warnings.filterwarnings('ignore')
nltk.download('punkt')
nltk.download('punkt_tab')

article = Article('https://en.wikipedia.org/wiki/Artificial_intelligence')
article.download()
article.parse()
article.nlp()
corpus = article.text

text = corpus
sentences = nltk.sent_tokenize(text)
