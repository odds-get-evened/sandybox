import math
import os
import pickle
import struct
import time
import unittest
from pathlib import Path

import numpy as np

from org.odds import rand
from org.odds.material.modeling import BaseModel
from org.odds.util import crc32


class NodeNetwork:
    def __init__(self, models_path: Path = None, num_nodes: int = 31, trainer=True):
        self.model = None

        # are we training models or reusing an existing?
        self.is_training = trainer

        self.len = num_nodes

        """
        a directory that stores all models
        """
        self.model_path: Path = Path(os.path.expanduser('~'), '.databox', 'material',
                                     'models') if not models_path else models_path
        # build storage path if it doesn't exist
        if not self.model_path.exists():
            self.model_path.mkdir(parents=True, exist_ok=True)

        self.id: bytes = crc32(os.urandom(64))

        """
        this is a list of nodes
        the standard for a node is a list of lists containing 4
        float values. values by index:
        0 is weight (is initialized as a random value between -1 and 1)
        1 is input value (this is a trained value, using models of each individual
            iteration to establish all node inputs)
        2 is output_true
        3 is output_false
        """
        self.nodes = []

    def start(self):
        self.nodes = self.generate_nodes()
        if self.is_training:
            print("training enabled")
            self.train()

        fs = list(self.model_path.glob("*.pkl"))
        if len(fs) > 0:
            cur = max(fs, key=lambda x: x.stat().st_birthtime)
            print(f"found a model at {cur.__str__()}")
            with open(cur, 'rb') as f:
                mdl = pickle.load(f)

            predicted_wgts = mdl.predict(np.array(self.nodes))
            input_wgts = [_ for _ in predicted_wgts]

            print(f"establishing {len(input_wgts)} input(s) for {len(self.nodes)} nodes")
            if len(input_wgts) == len(self.nodes):
                for i in range(len(self.nodes)):
                    self.nodes[i][1] = float(input_wgts[i])

            print(self.nodes[:10])

    def generate_nodes(self):
        # build network structure
        return [
            [rand.random_secrets(-1, 1)] +
            [math.nan for _ in range(3)]
            for _ in range(self.len)
        ]

    def train(self):
        # acquire latest model if one exists
        existing_models = list(self.model_path.glob("*.pkl"))

        if existing_models:
            # acquire the most recent model file
            recent_model = max(existing_models, key=lambda x: x.stat().st_birthtime)
            print(f'a model exists at {recent_model.__str__()}.')
            # read in model
            with open(recent_model, 'rb') as f:
                model = pickle.load(f)
            # gather only node weights
            # weights = [w[0] for w in self.nodes]

            # X = np.array(weights).reshape(-1, 1)
            X = np.array(self.nodes)
            # y = [rand.gaussian(-1, 1) for _ in weights]
            y = [rand.gaussian(-1, 1) for _ in range(len(self.nodes))]
            # training
            model.fit(X, y)

            # save retrained model to file
            pkl_fname = f"material-model-{crc32(struct.pack(">i", int(time.time()))).decode()}.pkl"
            fname = self.model_path.joinpath(pkl_fname)
            with open(fname, 'wb') as f:
                pickle.dump(model, f)
            print(f"material model updated and written to {fname.__str__()}.")
        else:
            print('no existing models found...')
            print('creating new model...')
            # determine appropriate model based on distribution variance
            # weights = [w[0] for w in self.nodes]
            model = BaseModel([w[0] for w in self.nodes]).model

            # reshaping weights for feature matrix
            # X = np.array(weights).reshape(-1, 1)
            X = np.array(self.nodes)
            # random dataset for initial training
            y = [rand.gaussian(-1, 1) for _ in range(len(self.nodes))]
            # training
            model.fit(X, y)

            # save model
            pkl_fname = f"material-model-{crc32(struct.pack(">i", int(time.time()))).decode()}.pkl"
            fname = self.model_path.joinpath(pkl_fname)
            with open(fname, 'wb') as f:
                pickle.dump(model, f)
            print(f"material model written to {fname.__str__()}.")
