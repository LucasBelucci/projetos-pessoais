from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar o webdriver (certifique-se de que o ChromeDriver ou outro driver esteja corretamente instalado)
driver = webdriver.Chrome()

# Acessar a página
driver.get("https://events.pokemon.com/en-us/events?near=Itu,%20SP,%20Brazil")

# Esperar até que o elemento com a classe 'event-listing' esteja visível
try:
    events = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.event-listing'))
    )


    # Agora que os eventos estão carregados, você pode extrair as informações
    for event in events:
        name = event.find_element(By.CLASS_NAME, 'event-name').text
        date = event.find_element(By.CLASS_NAME, 'event-date').text
        location = event.find_element(By.CLASS_NAME, 'event-location').text
        print(f"Nome: {name}, Data: {date}, Local: {location}")

except Exception as e:
    print('Erro ao encontrar o elemento: ', e)

finally:
    driver.quit()  # Fecha o navegador
