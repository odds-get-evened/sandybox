import math
import os
from itertools import zip_longest

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from org.odds import rand
from org.odds.util import crc32


class NodeIO:
    INPUT = 1
    OUTPUT = -1


class NodeMap:
    WEIGHT = 0


class SimpleNetwork:
    def __init__(self, ident: bytes, w: int = 64, h: int = 32):
        self.model = None
        self.id = ident
        self.h = h
        self.w = w

        self.layers = []

        self.mold()

    def mold(self):
        for i in range(self.h):
            self.layers.append([
                [
                    round(rand.random_secrets(-1, 1), 18),
                    list([math.nan for _ in range(3)])
                ] for _ in range(self.w)
            ])

        self.construct_ios()
        [print(lyr) for lyr in self.layers]
        # self.analysis()

    def construct_ios(self):
        # get a list of all the node weights in the layers
        weights = []  # get out weights somehow???
        # grab the weights' standard deviation
        std = float(np.std(weights))
        # train and return weights mapped to training result
        train_res = list(self.train(weights, std))

        # set all node input values to predicted value from training
        for wgt_pred in train_res:
            for i in range(len(self.layers)):
                for j in range(len(self.layers[i])):
                    if self.layers[i][j][0] == wgt_pred[0]:
                        self.layers[i][j][1][0] = wgt_pred[1]

        # now process the input somehow to generate both outputs

    def node(self, wgt):
        """
        find a node by its weight value
        Parameters
        ----------
        wgt weight value

        Returns list
        -------

        """
        for lyr in self.layers:
            for n in lyr:
                if n[0] == wgt:
                    return n

    def analysis(self):
        # extract weigths from nodes into list
        weights = [node[0] for lyr in self.layers for node in lyr]

        # print(weights)
        mean_wgt = np.mean(weights)
        print(f"mean: {mean_wgt}")
        std_wgt = np.std(weights)
        print(f"standard deviation: {std_wgt}")
        min_wgt = np.min(weights)
        print(f"minimum: {min_wgt}")
        max_wgt = np.max(weights)
        print(f"maximum: {max_wgt}")

        # plot it
        plt.hist(weights, bins=100, edgecolor='black')
        plt.title('distribution of node weights')
        plt.xlabel('weight')
        plt.ylabel('frequency')
        plt.show()

    def train(self, weights, std):
        self.model = self.model_selection(std)

        # prep data (reshaping the weights for ML input)
        X = np.array(weights).reshape(-1, 1)  # feature matrix (weights)
        y = [rand.gaussian(-1, 1) for _ in weights]  # random data for now

        # train the selected model and generate predictive results
        self.model.fit(X, y)

        predictions = self.model.predict(X)

        # for wgt, predict in zip(weights, prediction):
        #       print(f"weight: {wgt}, prediction: {predict}")

        return zip_longest(weights, predictions.tolist(), fillvalue=None)

    def model_selection(self, w):
        if w < 0.1:  # low variance, consistent data
            print("using `logistic regression` due to low variance")
            return LogisticRegression()

        elif w > 0.5:  # high variance, as data is too spread out
            print('using random forest regression, due to high variance')
            return RandomForestRegressor()

        else:
            print('using SVC for moderate variance')
            return SVC()


def main():
    material = SimpleNetwork(crc32(os.urandom(64)))
    # material.analyze()
    '''
    [(weight, (input, output+, output-)), ...]
    '''


if __name__ == "__main__":
    main()
