"""
Step 3

preparing the dataset with pandas and numpy
"""
import re

import pandas as pd
from sklearn.preprocessing import LabelEncoder

CHAR_NAME_PATTERN = re.compile(r"^(?P<char>\w+):")


def prepare_dataset(feature_set):
    labels = []

    for sentence in feature_set:
        print(type(sentence))
        match = CHAR_NAME_PATTERN.match(sentence)

        if match:
            char = match.group('char')
            labels.append(char)
        else:
            labels.append('Narration')  # non-dialogue sentences

    # encode labels into numerical values
    lbl_enc = LabelEncoder()
    y = lbl_enc.fit_transform(labels)

    df = pd.DataFrame(feature_set[0], columns=feature_set[1])
    df['label'] = y

    return df
