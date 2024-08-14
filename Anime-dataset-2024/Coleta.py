import requests
import json
import datetime
import os
import pandas as pd
import sqlalchemy


class Collector:
    def __init__(self, url, client_id):
        self.url = url
        self.instance = url.strip('&').split('=')[2]    # LIMIT
        self.type = url.strip('?').split('ranking_type=')[1] 
        self.type = self.type.split('&')[0] # RANK TYPE

    def get_endpoints(self, **kwargs):
        resp = requests.get(url, headers={'X-MAL-CLIENT-ID': client_id})
        print(resp)
        return resp
    
    def save_data(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        data['ingestion_time'] = datetime.datetime.now().strftime("%Y-%m%d %H:%M:%S")
        filename = f'Anime-dataset-2024/DadosColetados/{self.type}/{self.type}_{self.instance}_{now}.json'
        with open(filename, "w") as open_file:
            json.dump(data, open_file)

    def get_and_save(self, **kwargs):
        resp = self.get_endpoints(**kwargs)
        if resp.status_code == 200:
            data = resp.json()
            self.save_data(data)
            return data
        else:
            print(f'Erro')


client_id = '9b3882b98fa1b7771c34c38542be597a'
type = ['all', 'airing', 'upcoming', 'tv', 'ova', 'movie', 'special', 'bypopularity', 'favorite']
limit = [3, 10, 100, 500]

url_anime = 'https://api.myanimelist.net/v2/anime/5114?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'

url = 'https://api.myanimelist.net/v2/anime/10000?fields=rank,mean,alternative_titles'


#for tipo in type:
#    for limite in limit:
#        url_rank = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type={tipo}&limit={limite}'
#        collector = Collector(url_rank, client_id)
#        collector.get_and_save()

#https://myanimelist.net/apiconfig/references/api/v2#operation/anime_ranking_get
#https://myanimelist.net/forum/?topicid=1973077

#json_data = []

#with open("Anime-dataset-2024/DadosColetados/all/all_500_20240501_114345.529894.json") as json_file:
#    json_data = json.load(json_file)
    
json_file_path = "Anime-dataset-2024/DadosColetados/all/all_100_20240501_114344.273246.json"
node_id = []

with open(json_file_path, 'r') as j:
    contents = json.loads(j.read())
    contents_normalize = pd.json_normalize(contents, 'data')
    node_id = contents_normalize['node.id']
    
#content_list = list(contents_normalize.values())
#print(node_id)
#for i, node in zip(range(0,100), node_id):
    
#    print(f"{i}: {node}")

#feature3 = [d.get('id') for d in contents]

#node_id = [52991, 5114, 9253, 28977, 38524, 39486]
#node_id = [52991, 5114, 9253]
#filename = f'Anime-dataset-2024/DadosColetados/Details/top100/top100.json'
for i, node in zip(range(1,101), node_id):
    #print(node)

    url_anime = f'https://api.myanimelist.net/v2/anime/{node}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,studios,statistics'
    #print(url_anime)
    resp = requests.get(url_anime, headers={'X-MAL-CLIENT-ID': client_id})
    resp.raise_for_status()
    
    anime = resp.json()
    #print(anime)
    
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
    anime['ingestion_time'] = datetime.datetime.now().strftime("%Y-%m%d %H:%M:%S")
    filename = f'Anime-dataset-2024/DadosColetados/Details/{i}_{node}_{now}.json'
    
    #resp.close()
    with open(filename, "w") as open_file:
        json.dump(anime, open_file)

#        collector = Collector(url_rank, client_id)
#        collector.get_and_save()
