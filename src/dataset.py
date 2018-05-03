

import numpy as np
import os
import json
import pickle as pkl
import feature_extraction
import html_lastfm_parser


#инициализация json-а и фитч для плейлиста 1 пользователя


def init_features(parser_params, f_extr_params):

	info = html_lastfm_parser.get_json(
				path_from=parser_params['path_from'])

	exceptions = []
	for track in info:
		if not track['tags']:
			exceptions.append(track['file_name'])
		else:
			track['features'] = f_extr_params['path_to'] + track['file_name'][:-4] + '.pkl'

	html_lastfm_parser.dump(
		info= info, 
		path=parser_params['path_to'], 
		user_id=parser_params['user_id']) #TODO Нужно, чтобы номер брался путём прибавления 1 к последнему.

	feature_extraction.extract_features(
		path_from= f_extr_params['path_from'], 
			path_to= f_extr_params['path_to'], 
				tmp_path_for_wavs= f_extr_params['tmp_path_for_wavs'],
					exceptions= exceptions,
						separator= ['separator'], 
							methode = ['methode'], 
								linear = ['linear'])


# собирает выборку в окончательный вид


def make_dataset(json_name):
	
	#TODO нужно проходить по всем папкам, всех пользователей, вытаскивать json и по нему вытаскивать фитчи для треков
    
    X, Y = [], []
    meta = json.load(open(json_name))
    for sample in meta:
        features_file  = sample['features']
        features = pickle.load(open(features_file, "rb" ))
        X.append(features)
        Y.append(sample['tags'])#TODO сделать препроцессинг тегов
    return np.asarray(X), np.asarray(Y)

