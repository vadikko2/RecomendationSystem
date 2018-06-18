
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, r'../')
import src.dataset as ds
import os
import json
import src.html_lastfm_parser as hlp


# In[2]:


def read_json(path, filename):
    with open(path+filename) as f:
        return json.load(f)


# In[8]:


def init_features(path_with_infos = '../jsons/'):
    for file_info in os.listdir(path_with_infos):#идем по файлам info.json
        user_id = tracks=file_info[:-10]
        f_extr_params = {
            'path_from':"../tracks/{tracks}/".format(tracks=user_id),
            'path_to':"../mfccs/",
            'tmp_path_for_wavs':"../wavs/",
            'separator':"/",
            'methode':"mfcc",
            'linear':True
        }
        info = read_json(path_with_infos, file_info)#считываем
        info = ds.init_features(info, f_extr_params=f_extr_params)#вытаскиваем фитчи и добавляем в json адрес с фитчами
        hlp.dump(info, path_with_infos, user_id)#пересохраняем обновленный json


# In[4]:


def get_dataset(path_with_infos='../jsons/'):
    co_occ = hlp.load_co_occ()
    X, dY = ds.make_dataset_for_classifier(path_with_jsons=path_with_infos)
    Y = []
    for y in dY:
        Y.append(co_occ, y)
    Y = np.asarray(Y)
    return X, Y

