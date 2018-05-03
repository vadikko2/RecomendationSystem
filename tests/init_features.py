import sys
sys.path.insert(0, r'../')
import src.dataset as ds

parser_params = {
	'path_from':"../tracks/",
	'path_to':"../jsons/",
	'user_id': 1
}

f_extr_params = {
	'path_from':"../tracks/",
	'path_to':"../mfccs/",
	'tmp_path_for_wavs':"../wavs/",
	'separator':"/",
	'methode':"mfcc",
	'linear':True
}

ds.init_features(parser_params=parser_params, f_extr_params=f_extr_params)