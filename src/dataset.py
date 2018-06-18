import numpy as np
import os
import json
import pickle as pkl
import src.feature_extraction as fe
import src.html_lastfm_parser as hlp


#инициализация json-а и фитч для плейлиста 1 пользователя


def init_features(info, f_extr_params):
    
    exceptions = []
    for track in info:
        if not track['tags']:
            exceptions.append(track['file_name'])
        else:
            track['features'] = f_extr_params['path_to'] + track['file_name'][:-4]

    fe.extract_features(
        path_from= f_extr_params['path_from'], 
            path_to= f_extr_params['path_to'], 
                tmp_path_for_wavs= f_extr_params['tmp_path_for_wavs'],
                    exceptions= exceptions,
                        separator= f_extr_params['separator'], 
                            methode= f_extr_params['methode'], 
                                linear= f_extr_params['linear'])

    return info


# собирает выборку в окончательный вид


def make_dataset_for_classifier(path_with_jsons):
    X, Y = [], []
    for json_name in os.listdir(path_with_jsons):
        meta = json.load(open(os.path.abspath(path_with_jsons+json_name)))
        for sample in meta:
            features_file  = sample['features']
            features = pkl.load(open(features_file, "rb" ))
            X.append(features)
            Y.append(sample['tags'])#TODO сделать препроцессинг тегов
    return X, Y


