# import the required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

#options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

driver.get("https://events.pokemon.com/en-us/events?near=Itu,%20SP,%20Brazil")

element = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".event-listing"))
)

events = driver.find_elements(By.CSS_SELECTOR, ".event-list")

extracted_events = []

for event in events:
    events_data = {
        "name": event.find_element(By.CLASS_NAME, "event-name").text,
        "date": event.find_element(By.CLASS_NAME, "event-date").text,
        "location": event.find_element(By.CLASS_NAME, "event-location").text,
    }

    extracted_events.append(events_data)

print(extracted_events)