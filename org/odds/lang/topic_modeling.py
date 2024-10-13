import os
from pathlib import Path

import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation

from sklearn.feature_extraction.text import CountVectorizer

NATURE_RWEMERSON = Path(os.path.expanduser('~'), ".databox", "texts", "nature-rwemerson.txt")


def download_if_missing(resource_name, resource_type='corpora'):
    try:
        nltk.data.find(f'{resource_type}/{resource_name}')
        print(f'resource {resource_name} already available')
    except LookupError:
        print(f'resource {resource_name} not found...downloading...')
        nltk.download(resource_name)


def load_text(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        return f.read()


def preprocess_text(t: str):
    sentences = sent_tokenize(t)
    tokens = [word_tokenize(sentence) for sentence in sentences]
    stop_words = set(stopwords.words('english'))
    processed_tokens = []

    for sentence in tokens:
        processed = [
            word.lower() for word in sentence
            if word.isalpha() and word.lower() not in stop_words
        ]
        processed_tokens.append(processed)

    return processed_tokens

def feature_extraction(proc_sentences: list[str], max_features: int = 10):
    vec = CountVectorizer(max_features=max_features)

    # X
    return vec.fit_transform(proc_sentences), vec


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"topic {topic_idx + 1}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        print()


def main():
    download_if_missing('punkt', resource_type='tokenizers')
    download_if_missing('stopwords')

    content = load_text(NATURE_RWEMERSON)

    processed_tokens = preprocess_text(content)

    processed_sentences = [' '.join(sentence) for sentence in processed_tokens]

    X = feature_extraction(processed_sentences, max_features=1000)

    # topic model
    lda = LatentDirichletAllocation(n_components=10, random_state=10)
    lda.fit(X[0])

    no_top_words = 10
    display_topics(lda, X[1].get_feature_names_out(), no_top_words)


if __name__ == "__main__":
    main()
