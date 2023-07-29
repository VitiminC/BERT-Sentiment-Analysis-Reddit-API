# ======================== Reddit Web Crawler =======================
import requests, sys
import pprint
import json
import copy
import re
# import emot
# from io import BytesIO
# import pytesseract
# from spellchecker import SpellChecker
# from PIL import Image
# from bs4 import BeautifulSoup
# from nltk import RegexpTokenizer

# ========================= Word2Vec Embedding ======================
import torch
import torch.nn as nn
import numpy as np
# import gensim
import os
import pickle
import warnings
import re
# from gensim.models import Word2Vec, FastText
import matplotlib.pyplot as plt
import nltk
from nltk import RegexpTokenizer
from sklearn.metrics import *

# from allennlp.commands.elmo import ElmoEmbedder

# ========================== Text Cleaning ===========================

import pandas as pd
import datetime
import pymysql
import matplotlib
import bs4
import csv
import pandas
import numpy as np
from collections import Counter
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import shutil
from collections import defaultdict
from skimage.transform import resize
from skimage import io
import Levenshtein
from textblob import TextBlob

# ==================== Emotion detector ====================

import logging

logging.disable(logging.CRITICAL)
import os
import random
# from test_tube import HyperOptArgumentParser
# from transformers import DistilBertModel, DistilBertForSequenceClassification, DistilBertConfig
import torch
# from transformers import DistilBertTokenizer
# import pytorch_lightning as pl
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.data.distributed import DistributedSampler



URL_PATTERN = r'(https?:\/\/(?:www\.|(?!www|WAP))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www|WAP\.|(?!www|WAP))[a-zA-Z0-9]+\.[^\s]{2,}|www|WAP\.[a-zA-Z0-9]+\.[^\s]{2,})'
SUBREDDIT_PATTERN = r'(/?\s*[uUrR]\s*.*)*'
EXTRACT_URL_CAPTION_PATTERN = r'\[(.*)\]\s*\({}\).*'.format(URL_PATTERN)
EXTRACT_SUBREDDIT_CAPTION_PATTERN = r'\[(.*)\]\s*\({}\).*'.format(SUBREDDIT_PATTERN)
WHITESPACE_PATTERN = r'\s\s+'
NEWLINE_PATTERN = r'\n\t'
DELETE_REMOVE_PATTERN = r'^\[(deleted|removed)\]'


MYSQL_HOST = 'db-mysql-nyc1-97376-jun-18-backup-do-user-7545874-0.a.db.ondigitalocean.com'
MYSQL_USERNAME = 'doadmin'
MYSQL_PASSWORD = 'oie1nzcv745hf0sc'
MYSQL_PORT = 25060
MYSQL_DATABASE = 'defaultdb'


SUBMISSION_PATH = '/Users/karenyyy/Workspace/Emotion-recognition-dataset/stage_1_processed_subs'






