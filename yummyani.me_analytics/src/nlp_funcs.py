import re
import umap
import numpy as np
import pandas as pd
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from tqdm.auto import tqdm, trange
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA, TruncatedSVD

import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import pymorphy3

from bertopic import BERTopic
from transformers import DistilBertModel, DistilBertTokenizer
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification, pipeline

import torch
from torch.utils.data import DataLoader, TensorDataset

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# TF-IDF 
#######################################################################################################

def preprocess(x, morph, stop_words):
    x = x.lower()
    x = re.sub(r'\[/?[а-я]\]', '', x)
    x = re.sub(r'\[/?спойлер(?:=[^\]]+)?\]', '', x)
    x = re.sub(r'[^а-яёa-z0-9\s]', ' ', x)
    x = re.sub(r'\s+', ' ', x).strip()
    x = x.split()
    x = [w for w in x if w not in stop_words]
    x = [morph.parse(w)[0].normal_form for w in x]
    x = " ".join(x)
    return x


def plotly_plot(latent_2d, df, rand_idx):
    fig = px.scatter(x=latent_2d[:, 0], y=latent_2d[:, 1],
        hover_data={'comment': df.iloc[rand_idx]['text'].tolist()})
    fig.show()