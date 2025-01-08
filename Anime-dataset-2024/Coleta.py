# %%
import requests
import json
import datetime
import os
import pandas as pd
import sqlalchemy

# Configuração da API
client_id = '9b3882b98fa1b7771c34c38542be597a'

# %%

class Collector:
    def __init__(self, url, client_id):
        self.url = url
        self.instance = url.strip('&').split('=')[2]    # LIMIT
        self.type = url.strip('?').split('ranking_type=')[1] 
        self.type = self.type.split('&')[0] # RANK TYPE

    def get_endpoints(self, **kwargs):
        resp = requests.get(self.url, headers={'X-MAL-CLIENT-ID': client_id})
        print(resp)
        return resp
    
    def save_data(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        data['ingestion_time'] = datetime.datetime.now().strftime("%Y-%m%d %H:%M:%S")
        directory = f'Anime-dataset-2024/DadosColetados/{self.type}/'
        os.makedirs(directory, exist_ok=True) # Cria o diretório se não existir
        filename = f'Anime-dataset-2024/DadosColetados/{self.type}/{self.type}_{self.instance}_{now}.json'

        # Tenta abrir o arquivo ou criar um novo
        try:
            with open(filename, "r") as json_file:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    existing_data = [] # Garante que será uma lista
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = [] # Se o arquivo não existir ou estiver vazio, inicia uma lista vazia
        
        # Adiciona novos dados à lista existente

        existing_data.append(data)

        # Escreve todos os dados no arquivo
        with open(filename, "w") as open_file:
            json.dump(existing_data, open_file, indent=4)
            print(f"Data appended to {filename} file.")

    def get_and_save(self, **kwargs):
        resp = self.get_endpoints(**kwargs)
        if resp.status_code == 200:
            data = resp.json()
            self.save_data(data)
            return data
        else:
            print(f'Erro')

# Configuração da API
client_id = '9b3882b98fa1b7771c34c38542be597a'

# Definição dos tipos e dos limites de ranking
type = ['all', 'airing', 'upcoming', 'tv', 'ova', 'movie', 'special', 'bypopularity', 'favorite']
limit = [3, 10, 100, 500]


# Execução de cada combinação para tipo e limite
for tipo in type:
    for limite in limit:
        url_rank = f'https://api.myanimelist.net/v2/anime/ranking?ranking_type={tipo}&limit={limite}'
        collector = Collector(url_rank, client_id)
        collector.get_and_save()

# %%    
# import json
json_file_path = "Anime-dataset-2024/DadosColetados/all/all_500_20250103_104237.844744.json"


url_anime = 'https://api.myanimelist.net/v2/anime/5114?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics'

url = 'https://api.myanimelist.net/v2/anime/10000?fields=rank,mean,alternative_titles'


with open(json_file_path, 'r') as j:
    contents = json.loads(j.read())
    contents_normalize = pd.json_normalize(contents, 'data')
    node_id = contents_normalize['node.id']
    

save_directory = 'Anime-dataset-2024/DadosColetados/Details/'

os.makedirs(save_directory, exist_ok=True)

for i, node in zip(range(1,101), node_id):

    url_anime = f'https://api.myanimelist.net/v2/anime/{node}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,studios,statistics'
    resp = requests.get(url_anime, headers={'X-MAL-CLIENT-ID': client_id})
    resp.raise_for_status()
    
    anime = resp.json()
    
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
    anime['ingestion_time'] = datetime.datetime.now().strftime("%Y-%m%d %H:%M:%S")

    filename = os.path.join(save_directory, f'{i}_{node}_{now}.json')
    
    with open(filename, "w") as open_file:
        json.dump(anime, open_file, indent=4)

# %%
'''
import os

json_file_path = "Anime-dataset-2024/DadosColetados/all/all_500_20250103_104237.844744.json"

if os.path.exists(json_file_path):
    print("Arquivo encontrado!")

else:
    print(f"Arquivo não encontrado: {json_file_path}")
'''
