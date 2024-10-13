from sklearn.feature_extraction.text import CountVectorizer

"""
Step 2

feature extraction
"""


def feature_extraction(proc_tokens: list[list[str]]):
    proc_sentences = [' '.join(sent) for sent in proc_tokens]

    # initialize this thing muhahaha
    vectorizer = CountVectorizer(max_features=1000)

    X = vectorizer.fit_transform(proc_sentences)

    # convert to numpy array
    X = X.toarray()

    # get feature names for reference
    # return vectorizer.get_feature_names_out()
    return X, vectorizer.get_feature_names_out()
