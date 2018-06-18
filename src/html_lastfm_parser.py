
# coding: utf-8

# In[1]:


import requests as req
import lxml.html
import json
import re, os
import pickle
import codecs
import operator
import numpy as np


# In[2]:


def tags_filter(tags, artist, track):
    filtered = []
    garbage = [str(i) for i in range(10)]
    for tag in tags:
        check = True
        for g in garbage:
            if (g in tag) or (artist in tag) or (track in tag):
                check = False
                break
        if check:
            filtered.append(tag)
    return filtered


# In[3]:


def get_song_tags(artist = "", track = ""):
    tmp_artist = artist.lower().replace(' ', '+')
    tmp_track = track.lower().replace(' ', '+')
    url = f'https://www.last.fm/music/{tmp_artist}/_/{tmp_track}'
    html_from_last_fm = req.get(url).text
    html = lxml.html.fromstring(html_from_last_fm)
    track_dict = {'artist': artist, 'track': track, 'tags':[]}
    for li in html.xpath("//ul[@class='tags-list tags-list--global']/li"):
        track_dict['tags'].append(str(li.text_content().lower().replace('-', ' ')))
    track_dict['tags'] = tags_filter(track_dict['tags'], tmp_artist, tmp_track)
    print('{artist}-{track} tags was parsed: {tags}'.format(artist=artist, track=track, tags=track_dict['tags']))
    return track_dict


# In[4]:


def get_track_list(path):
    for file in os.listdir(path):
        track_info = re.split('[-]', file[:-4])
        if track_info[0][-1] == ' ':
            track_info[0] = track_info[0][:-1]
        if track_info[1][0] == ' ':
            track_info[1] = track_info[1][1:]
        yield track_info[0], track_info[1], file


# In[5]:


def get_json(path):
    info = []
    for artist, track, file_name in get_track_list(path):
        meta = get_song_tags(artist= artist, track= track)
        meta['file_name'] = file_name
        if meta['tags']:
            info.append(meta)
    return info


# In[6]:


def dump(info, path, user_id):
    with open(path+f'{user_id}_info.json', 'w') as fp:
        json.dump(info, fp, sort_keys=True, indent=4)


# In[7]:


def load_ganres(path):
    for filename in os.listdir(os.path.abspath(path)):
        sub_ganres = []
        with open(os.path.abspath(path)+'\\'+filename, 'r') as f:
            yield filename[:-4], [tag.lower().replace('-', ' ') for tag in f.read().split('\n')]


# In[8]:


def dump_ganres_co_occ(co_occ_path, co_occ):
    with open(co_occ_path+'ganresCoOcc.pkl', 'wb') as f:
        pickle.dump(co_occ, f, pickle.HIGHEST_PROTOCOL)    


# In[9]:


def init_ganres_co_occ(path, co_occ_path):
    co_occ = {}
    for ganre, sub_ganres in load_ganres(path):
        for sg in sub_ganres:
            co_occ[sg] = 0
    dump_ganres_co_occ(co_occ_path, co_occ)
    return co_occ


# In[10]:


def who_exist(co_occ_el, tags):
    first = co_occ_el.keys()
    result = []
    for t in tags:
        if t in first:
            result.append(t)
    return result


# In[11]:


def update_ganres_co_occ(co_occ, dataset_json):
    for song in dataset_json:
        tags = song['tags']
        existed = who_exist(co_occ, tags)
        if len(existed):
            for tag in tags:
                if tag in existed:
                    co_occ[tag]+=1
                else:
                    co_occ[tag] = 1
    return co_occ


# In[12]:


def init_co_occ_matrix(path_with_ganres='..\\ganres_full\\', path_to_save='..\\'):
    co_occ = init_ganres_co_occ(path=path_with_ganres, co_occ_path=path_to_save)
    print(co_occ)
    return co_occ


# In[13]:


def update_co_occ_matrix(co_occ, path_with_tracks='..\\tracks\\', path_to_save_info='..\\jsons\\', path_to_save_co_occ='..\\'):
    for folder in os.listdir(path_with_tracks):
        info = get_json('{path}{folder}\\'.format(folder=folder, path=path_with_tracks))
        dump(info, path_to_save_info, folder)
        co_occ = update_ganres_co_occ(co_occ, info)
        dump_ganres_co_occ(path_to_save_co_occ, co_occ)
        dump(co_occ,path_to_save_co_occ, 'co_occ')
    return co_occ


# In[14]:


def load_co_occ(path='..\\', filename='ganresCoOcc.pkl'):
    with open(path+filename, 'rb') as f:
        co_occ = pickle.load(f)
    co_occ = sorted(co_occ.items(), key=operator.itemgetter(1))
    co_occ.reverse()
    return co_occ


# In[15]:


def get_y(co_occ, tags):
    y = np.zeros(len(co_occ))
    for tag in tags:
        for i in range(len(co_occ)):
            if co_occ[i][0] == tag:
                y[i] = 1
                break
    return y

