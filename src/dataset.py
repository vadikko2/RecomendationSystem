

import numpy as np
import os
import json
import pickle as pkl


# собирает выборку в окончательный вид


def make_dataset(json_name):
    X, Y = [], []
    meta = json.load(open(json_name))
    for sample in meta:
        features_file  = sample['features']
        features = pickle.load(open(features_file, "rb" ))
        X.append(features)
        Y.append(sample['tags'])#TODO сделать препроцессинг тегов
    return np.asarray(X), np.asarray(Y)

