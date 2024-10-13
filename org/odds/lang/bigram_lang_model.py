import os
import random
from collections import defaultdict, Counter
from pathlib import Path

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

NATURE_RWEMERSON = Path(os.path.expanduser('~'), ".databox", "texts", "nature-rwemerson.txt")


def download_if_missing(resource_name, resource_type='corpora'):
    try:
        nltk.data.find(f'{resource_type}/{resource_name}')
        print(f'resource {resource_name} already available')
    except LookupError:
        print(f'resource {resource_name} not found...downloading...')
        nltk.download(resource_name)


def preprocess_text(t: str):
    tokens = word_tokenize(t)
    stop_words = set(stopwords.words('english'))

    processed_tokens = [
        word.lower() for word in tokens
        if word.isalpha() and word.lower() not in stop_words
    ]

    return processed_tokens


def generate_bigram_model(tokens: list[str]):
    model = defaultdict(Counter)

    for i in range(len(tokens) - 1):
        cur = tokens[i]
        next = tokens[i + 1]
        model[cur][next] += 1

    return model


def generate_text(model, start_word, length=10):
    cur_word = start_word
    generated = [cur_word]

    for _ in range(length):
        next_words = model.get(cur_word, None)

        if not next_words:
            break
        next_word = random.choices(list(next_words.keys()), weights=list(next_words.values()))[0]
        generated.append(next_word)
        cur_word = next_word

    return ' '.join(generated)


def main():
    download_if_missing('punkt', 'tokenizers')
    download_if_missing('stopwords')

    with open(NATURE_RWEMERSON, 'r', encoding='utf8') as f:
        content = f.read()
    tokens = preprocess_text(content)

    bigram_model = generate_bigram_model(tokens)
    start_word = random.choice(tokens)
    sample_text = generate_text(bigram_model, start_word, length=100)
    print(sample_text)


if __name__ == "__main__":
    main()
