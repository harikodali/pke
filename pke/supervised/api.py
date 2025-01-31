# -*- coding: utf-8 -*-

""" Abstract base class for Supervised models. """

from __future__ import division
from __future__ import absolute_import

import os
from time import time
from pke.base import LoadFile
from sklearn.preprocessing import MinMaxScaler
from joblib import load as load_model


class SupervisedLoadFile(LoadFile):
    """ The SupervisedLoadFile class that provides extra base functions for
        supervised models. """

    def __init__(self):
        """ Redefining initializer. """

        super(SupervisedLoadFile, self).__init__()

        self.instances = {}
        """ The instances container. """

    def feature_scaling(self):
        """ Scale features to [0,1]. """

        candidates = self.instances.keys()
        X = [self.instances[u] for u in candidates]
        X = MinMaxScaler().fit_transform(X)
        for i, candidate in enumerate(candidates):
            self.instances[candidate] = X[i]

    def feature_extraction(self):
        """ Skeleton for feature extraction. """
        pass

    def classify_candidates(self, model=None):
        """ Classify the candidates as keyphrase or not keyphrase.

            Args:
                model (str): the path to load the model in pickle format,
                    default to None.
        """
        # get matrix of instances
        candidates = self.instances.keys()
        X = [self.instances[u] for u in candidates]

        # classify candidates
        y = model.predict_proba(X)

        for i, candidate in enumerate(candidates):
            self.weights[candidate] = y[i][1]

    def candidate_weighting(self):
        """ Extract features and classify candidates with default parameters."""
        if not self.candidates:
            return

        self.feature_extraction()
        self.classify_candidates()
