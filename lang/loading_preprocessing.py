import os
from pathlib import Path

import nltk
import pandas as pd
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pandas import DataFrame

from lang.feature_extraction import feature_extraction

"""
Step 1

loading and preprocessing the text
"""

nltk_data = Path(os.environ.get('NLTK_DATA'))

nltk.data.path.clear()
nltk.data.path.append(nltk_data.__str__())

NATURE_RWEMERSON = Path(os.path.expanduser('~'), ".databox", "texts", "nature-rwemerson.txt")


def preprocess_text(s):
    sentences = sent_tokenize(s)

    # further tokenize each sentence into words
    tokens = [word_tokenize(sentence) for sentence in sentences]

    # convert to lower case, remove punctuation, and remove stopwords
    stop_words = set(stopwords.words('english'))
    processed_tokens = []

    for sentence in tokens:
        processed = [
            word.lower()
            for word in sentence
            if word.isalpha() and word.lower() not in stop_words
        ]
        processed_tokens.append(processed)

    return processed_tokens


def main():
    with open(NATURE_RWEMERSON, 'r', encoding='utf8') as f:
        s = f.read()
    # 1.
    tokened_sentences = preprocess_text(s)
    # 2.
    X, features = feature_extraction(tokened_sentences)
    # 3
    df: DataFrame = pd.DataFrame

if __name__ == "__main__":
    main()
