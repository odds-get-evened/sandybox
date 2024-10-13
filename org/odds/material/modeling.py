from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


class BaseModel:
    def __init__(self, weights: list[Any]):
        self.weights = weights
        std = float(np.std(self.weights))
        self.model = self.determine_model(std)

    def determine_model(self, std):
        if std < 0.1:  # low variance, consistent data
            print("using `logistic regression` due to low variance")
            return LogisticRegression()

        elif std > 0.5:  # high variance, as data is too spread out
            print('using random forest regression, due to high variance')
            return RandomForestRegressor()

        else:
            print('using SVC for moderate variance')
            return SVC()
