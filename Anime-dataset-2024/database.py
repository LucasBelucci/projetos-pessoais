import os
import json
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


def create_connection():
    #connection = None
    print('conexão')
    try:
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = "anime_db"
        )

        
        #if connection.is_connected():
        #print('Conexão com MySQL bem-sucedida')
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database não existe")
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Usuário ou senha inválido")
        else:
            print(error)        
    return mydb

def create_table():
    try:
        mydb = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = "anime_db"
        )
        if mydb.is_connected():

            cursor = mydb.cursor()
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS anime_details(
                id INT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                start_date DATE,
                end_date DATE,
                synopsis TEXT,
                mean FLOAT,
                `rank` INT,
                popularity INT,
                num_list_users INT,
                num_scoring_users INT,
                nsfw VARCHAR(100),
                created_at DATE,
                updated_at DATE,
                media_type VARCHAR(100),
                status VARCHAR(100),
                genres VARCHAR(100),
                num_episodes INT,
                source VARCHAR(100),
                average_episode_duration INT,
                rating VARCHAR(100),
                pictures VARCHAR(100),
                background VARCHAR(100),
                studios VARCHAR(100),
                ingestion_time DATETIME,
                main_picture_medium VARCHAR(100),
                main_picture_large VARCHAR(100),
                alternative_titles_synonyms VARCHAR(100),
                alternative_titles_en VARCHAR(100),
                alternative_titles_ja VARCHAR(100),
                start_season_year INT,
                start_season_season VARCHAR(100),
                statistics_status_watching VARCHAR(100),
                statistics_status_completed VARCHAR(100),
                statistics_status_on_hold VARCHAR(100),
                statistics_status_dropped VARCHAR(100),
                statistics_status_plan_to_watch VARCHAR(100),
                statistics_num_list_users INT,
                broadcast_day_of_the_week VARCHAR(100),
                broadcast_start_time VARCHAR(100)
                

            );
            '''

            cursor.execute(create_table_query)
            mydb.commit()

            cursor.execute("DESCRIBE anime_details")
            result = cursor.fetchall()
            for row in result:
                print(row)

    except mysql.connector.Error as error:
        print(error)
    
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()
            
            print('Conexão encerrada')
        #if connection.is_connected():
        #print('Conexão com MySQL bem-sucedida')
        

                

def insert_anime_data(connection, anime_data):
    cursor = connection.cursor()

    ingestion_time = anime_data.get('ingestion_time', '')
    if ingestion_time:
        try:
            if len(ingestion_time) == 18:  # Assumindo que o formato incorreto tenha 15 caracteres
                print('Entrei no IF INGESTION')
                corrected_date = ingestion_time[:4] + '-' + ingestion_time[5:7] + '-' + ingestion_time[7:9]
                corrected_time = ingestion_time[9:]
                ingestion_time = corrected_date + ' ' + corrected_time
                print(f"Ingestion time corrigido para: {ingestion_time}")  # Verifique a correção no log
            try:
                ingestion_time = datetime.strptime(ingestion_time, "%Y-%m-%d %H:%M:%S")
                print(f'Ingestion time formatado corretamente: {ingestion_time}')

            except ValueError as ve:
                print(f'Erro ao tentar converter ingestion_time para datetime: {ve}')
                ingestion_time = None
            except Exception as e:
                print(f'Erro inesperado ao processar ingestion_time: {e}')
                ingestion_time = None

        except Exception as e:
            print(f'Erro inesperado ao processar ingestion_time: {e}')
            ingestion_time = None

    insert_query = """INSERT INTO anime_details (
                        id, title, start_date, end_date, synopsis, mean, `rank`, popularity, num_list_users,
                        num_scoring_users, nsfw, created_at, updated_at, media_type, status, genres, num_episodes,
                        source, average_episode_duration, rating, pictures, background, studios, ingestion_time, main_picture_medium,
                        main_picture_large, alternative_titles_synonyms, alternative_titles_en, alternative_titles_ja,
                        start_season_year, start_season_season, statistics_status_watching, statistics_status_completed,
                        statistics_status_on_hold, statistics_status_dropped, statistics_status_plan_to_watch,
                        statistics_num_list_users, broadcast_day_of_the_week, broadcast_start_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(insert_query,(
            anime_data.get('id'),
            anime_data.get('title'),
            anime_data.get('start_date'),
            anime_data.get('end_date'),
            anime_data.get('synopsis'),
            anime_data.get('mean'),
            anime_data.get('rank'),
            anime_data.get('popularity'),
            anime_data.get('num_list_users'),
            anime_data.get('num_scoring_users'),
            anime_data.get('nsfw'),
            anime_data.get('created_at'),
            anime_data.get('updated_at'),
            anime_data.get('media_type'),
            anime_data.get('status'),
            ', '.join([genre.get('name', '') for genre in anime_data.get('genres', []) if isinstance(genre, dict)]),
            anime_data.get('num_episodes'),
            anime_data.get('source'),
            anime_data.get('average_episode_duration'),
            anime_data.get('rating'),
            ', '.join([pic.get('medium', '') for pic in anime_data.get('pictures', []) if isinstance(pic, dict)]),
            anime_data.get('background'),
            ', '.join([studio.get('name', '') for studio in anime_data.get('studios', []) if isinstance(studio, dict)]),
            #anime_data.get('ingestion_time'),
            ingestion_time,
            anime_data.get('main_picture', {}).get('medium'),
            anime_data.get('main_picture', {}).get('large'),
            ', '.join(anime_data.get('alternative_titles', {}).get('synonyms', [])),
            anime_data.get('alternative_titles', {}).get('en'),
            anime_data.get('alternative_titles', {}).get('ja'),
            anime_data.get('start_season', {}).get('year'),
            anime_data.get('start_season', {}).get('season'),
            anime_data.get('statistics', {}).get('status', {}).get('watching'),
            anime_data.get('statistics', {}).get('status', {}).get('completed'),
            anime_data.get('statistics', {}).get('status', {}).get('on_hold'),
            anime_data.get('statistics', {}).get('status', {}).get('dropped'),
            anime_data.get('statistics', {}).get('status', {}).get('plan_to_watch'),
            anime_data.get('statistics', {}).get('status', {}).get('num_list_users'),
            anime_data.get('broadcast', {}).get('day_of_the_week'),
            anime_data.get('broadcast', {}).get('start_time'),

        ))
        
        connection.commit()
        print(f"Dados do anime {anime_data['title']} inseridos com sucesso")
    except mysql.connector.Error as e:
        #print('')
        print(f'Erro ao inserir dados no MySQL: {e}')
        
def process_json_files(directory, connection):
    # Verificar se o argumento directory é uma string (o caminho do diretório)
    if isinstance(directory, str):
        print(f"Diretório de processamento: {directory}")
    else:
        print("Erro: O argumento 'directory' não é uma string.")
        return

    # Verificar se o diretório existe
    if not os.path.exists(directory):
        print(f"Erro: O diretório {directory} não foi encontrado.")
        return
    
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".json"):
            print('entrei')
            file_path = os.path.join(directory, filename)
            print(f"Processando o arquivo: {file_path}")
            with open(file_path, 'r') as file:
                anime_data = json.load(file)

                if isinstance(anime_data, list):
                    for anime_data_list in anime_data:
                        insert_anime_data(connection, anime_data_list)
                else:
                    insert_anime_data(connection, anime_data)
'''
'''
#if __name__ == "main":
json_directory = "Anime-dataset-2025"
print('main')
connection = create_connection()
print(connection)
if connection is not None:
    print('cheguei')
    process_json_files(json_directory, connection)
    connection.close()

#cursor.execute("CREATE DATABASE anime_db")

#create_table()
#insert_anime_data()