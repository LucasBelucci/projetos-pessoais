from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
#from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

'''


client = Client(account_sid, auth_token)



# Configurações do Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")

options.page_load_strategy = "none"

driver = Chrome(options=options)

service = Service('C:\\webdrivers\\chromedriver.exe')  # Substitua pelo caminho do seu ChromeDriver

driver.implicitly_wait(5)

# URL do site que você deseja monitorar


#url = "https://www.instacart.com/store/sprouts/collections/bread/872?guest=true"
url = "https://events.pokemon.com/en-us/events?sort=distance&maxDistance=100"

session = HTMLSession()

response = session.get(url)
response.html.render()
print(response.html)
#print(response.html.find('event-card'))

soup = BeautifulSoup(response.html.html, 'html.parser')

print(soup.find_all('article', class_='name-tag-holder'))

#driver.get(url)
#time.sleep(20)



service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

url = 'https://events.pokemon.com/en-us/events?sort=distance&maxDistance=100'
driver.get(url)


driver.find_elements(By.CLASS_NAME, 'event-card')

time.sleep(60)
'''
from flask import Flask, jsonify, make_response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/get_events')
def get_events():
    # URL da página correta
    url = 'https://events.pokemon.com/en-us/events?sort=distance&maxDistance=100'

    try:
        # Faz a requisição para a página
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins

        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Lista para armazenar os eventos
        eventos = []

        # Encontra todas as divs que contêm informações dos eventos
        eventos_divs = soup.find_all('div', class_='event-card')

        # Itera sobre cada div de evento e extrai nome e endereço
        for evento_div in eventos_divs:
            nome = evento_div.find('div', class_='event-title').text.strip()
            endereco = evento_div.find('div', class_='event-location').text.strip()
            eventos.append({'nome': nome, 'endereco': endereco})

        # Retorna os eventos como JSON
        return jsonify(eventos)
    except requests.exceptions.HTTPError as http_err:
        return make_response(jsonify({"error": f"HTTP error occurred: {http_err}"}), 500)
    except requests.exceptions.RequestException as req_err:
        return make_response(jsonify({"error": f"Request error occurred: {req_err}"}), 500)

if __name__ == '__main__':
    app.run(debug=True)

