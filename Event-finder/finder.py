'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from twilio.rest import Client

# Configurações do Twilio


client = Client(account_sid, auth_token)

# Configurações do Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar o Chrome em modo headless
service = Service('C:\\webdrivers\\chromedriver.exe')  # Substitua pelo caminho do seu ChromeDriver

# URL do site que você deseja monitorar
url = "https://events.pokemon.com/en-us/events?sort=distance&maxDistance=100"

# Função para obter os eventos do site
def obter_eventos():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(10)  # Aguarde o carregamento da página
    
    eventos = []
    eventos_divs = driver.find_elements(By.CLASS_NAME, 'event-card')
    for evento_div in eventos_divs:
        nome = evento_div.find_element(By.CLASS_NAME, 'event-title').text
        data = evento_div.find_element(By.CLASS_NAME, 'event-date').text
        local = evento_div.find_element(By.CLASS_NAME, 'event-location').text
        eventos.append({'nome': nome, 'data': data, 'local': local})
    
    driver.quit()
    return eventos

# Função para comparar eventos e identificar novos
def verificar_novos_eventos(eventos_antigos, eventos_novos):
    novos_eventos = []
    for evento in eventos_novos:
        if evento not in eventos_antigos:
            novos_eventos.append(evento)
    return novos_eventos

# Função para enviar mensagens via WhatsApp
def enviar_mensagem(eventos):
    for evento in eventos:
        message = client.messages.create(
            body=f"Nome: {evento['nome']}\nData: {evento['data']}\nLocal: {evento['local']}",
            from_=twilio_number,
            to=destination_number
        )
        print(f"Mensagem enviada: {message.sid}")

# Inicializa a lista de eventos
eventos_antigos = []

# Loop para rodar periodicamente
while True:
    eventos_novos = obter_eventos()
    novos_eventos = verificar_novos_eventos(eventos_antigos, eventos_novos)
    
    if novos_eventos:
        print("Novos eventos encontrados:")
        for evento in novos_eventos:
            print(f"Nome: {evento['nome']}, Data: {evento['data']}, Local: {evento['local']}")
 #       enviar_mensagem(novos_eventos)
        eventos_antigos = eventos_novos
    
    # Aguarda um tempo antes de fazer a próxima verificação (ex.: 10 minutos)
#    time.sleep(30)
'''
import requests

# URL do proxy local
proxy_url = 'http://localhost:5000/get_events'

# Faz a requisição para o proxy e obtém os dados
response = requests.get(proxy_url)
data = response.json()

# Itera sobre os eventos e imprime nome e endereço
for event in data:
    print(f"Nome: {event['name']}")
    print(f"Endereço: {event['location']}")
    print("-" * 30)
