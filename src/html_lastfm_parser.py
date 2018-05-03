
# coding: utf-8

# In[1]:


import requests as req
import lxml.html
import json
import re, os
import sys

# In[2]:


def get_song_tags(artist = "", track = ""):
    tmp_artist = artist.lower().replace(' ', '+')
    tmp_track = track.lower().replace(' ', '+')
    url = f'https://www.last.fm/music/{tmp_artist}/_/{tmp_track}'
    html_from_last_fm = req.get(url).text
    html = lxml.html.fromstring(html_from_last_fm)
    track_dict = {'artist': artist, 'track': track, 'tags':[]}
    for li in html.xpath("//ul[@class='tags-list tags-list--global']/li"):
        track_dict['tags'].append(li.text_content())
    return track_dict


# In[3]:


def get_track_list(path):
    for file in os.listdir(path):
        track_info = re.split('[-]', file[:-4])
        if track_info[0][-1] == ' ':
            track_info[0] = track_info[0][:-1]
        if track_info[1][0] == ' ':
            track_info[1] = track_info[1][1:]
        yield track_info[0], track_info[1], file


# In[8]:


def get_json(path):
    info = []
    #TODO добавить проверку на наличие тегов. Если нет тегов дальше ничего не делаем
    for artist, track, file_name in get_track_list(path):
        meta = get_song_tags(artist= artist, track= track)
        meta['file_name'] = file_name
        if meta['tags']:
            info.append(meta)
    return info


# In[5]:


def dump(info, path, user_id):
    with open(path+f'{user_id}_info.json', 'w') as fp:
        json.dump(info, fp)


def make_sample(path_from, path_to, user_number):
	info = get_json(path_from)# './/tracks//'
	dump(info,path_to, user_number)# '', 1
	#TODO После генерации фитч добавить в json поле 'features' чтобы можно было обращаться на прямую
if __name__ == '__main__':
	make_sample(sys.argv[1], sys.argv[2], int(sys.argv[3]))# './/tracks//', '', 1
	

