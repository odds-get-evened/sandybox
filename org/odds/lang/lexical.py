import asyncio
import re
import time
from concurrent.futures import ThreadPoolExecutor

import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, words

from hashies import big_end_int_64


class LexicalAnalyzer:
    def __init__(self, s: str, max_workers: int = 3):
        self.s = s
        self.max_workers = max_workers
        self.new_sents = []
        self.stop_words = stopwords.words('english')
        self.valid_words = words.words()

    def process(self):
        return asyncio.run(self.process_text())

    async def process_text(self):
        start_time = time.time()
        print(f'started processing text...')

        self.s = re.sub(r"[^\w\s]", '', self.s)
        # remove line breaks and extra spacing
        self.s = re.sub(r"[\r\n\s]+", ' ', self.s)

        sents = sent_tokenize(self.s)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            _loop = asyncio.get_event_loop()
            tasks = [_loop.run_in_executor(executor, self.process_sentence, sent) for sent in sents]
            self.new_sents = await asyncio.gather(*tasks)

        print(f"processing ended after {time.time() - start_time}s")
        return self.new_sents

    def process_sentence(self, s: str):
        tokens = [token for token in word_tokenize(s)]

        _words = [
            word for word in tokens
            if word not in self.stop_words
               and word in self.valid_words
               and len(word) > 1  # because there are no single letter non-stopwords
        ]

        return _words


def normalize_arr(arr: list, t_min=-1, t_max=1) -> list:
    """
    bring an array of number values within a bounds constraint
    :param arr:
    :param t_min:
    :param t_max:
    :return: a normalized list
    """
    norm_arr = []

    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)

    for i in arr:
        try:
            temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        except ZeroDivisionError:
            # using a midpoint value for division by zero handling
            # another approach is minimum value but i don't understand
            # how that effect relationships
            temp = ((t_min + t_max) / 2)

        norm_arr.append(temp)

    return norm_arr


def normalize_str(s: str, t_min=-1, t_max=1) -> list:
    """
    using a natural language model (NLTK), converting text
    into a list of normalized number values
    :param s:
    :param t_min:
    :param t_max:
    :return: a normalized list
    """
    # all to lowercase
    s = s.lower()
    # remove numbers
    s = re.sub(r'\d+', '', s)
    # remove everything except words and spaces
    s = re.sub(r"[^\w\s]", '', s)

    try:
        stopw = set(stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords', quiet=True)
        stopw = set(stopwords.words('english'))

    # remove stopwords and convert all strings to integer hash
    s_ls = [big_end_int_64(w.encode('utf8')) for w in s.split(' ') if w not in stopw]
    # normalize
    s_ls = normalize_arr(s_ls, t_min, t_max)

    return s_ls


def plots_2d(arr: list) -> list:
    """
    convert a 1 dimensional list to a 2 dimensional one, for plotting 2D coordinates
    :param arr:
    :return: a list of 2D coordinates
    """
    new_arr = []

    for i in range(len(arr)):
        plot = None

        if i * 2 < len(arr):
            plot = [arr[i * 2]]

        if i * 2 + 1 < len(arr):
            plot.append(arr[i * 2 + 1])

        if plot is not None:
            new_arr.append(plot)

    return new_arr


def plots_3d(arr: list) -> list:
    """
    converts a 1-dimensional list to a 2-dimensional one, for plotting 3D coordinates
    :param arr:
    :return: a list of 3D coordinates
    """
    new_arr = []

    # pad list length to be divisible by 3
    mod = len(arr) % 3
    if mod > 0:
        pad_size = 3 - mod
        arr += [0] * pad_size

    for i in range(len(arr)):
        plot = None

        if i * 3 < len(arr):
            plot = [arr[i * 3]]

        if i * 3 + 1 < len(arr):
            plot.append(arr[i * 3 + 1])

        if i * 3 + 2 < len(arr):
            plot.append(arr[i * 3 + 2])

        if plot is not None:
            new_arr.append(plot)

    return new_arr
