from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def setup():
    print("----- Setting Up -----")
    service = Service(r'C:\Users\YasserAITLAZIZ\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')  # change this path
    options = Options()
    options.headless = False  # Retirez le mode headless pour le débogage visuel
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch(driver):
    print("----- Fetching -----")
    url = "https://1xbet.ng/games-frame/games/371?co=85&cu=81&lg=en&wh=50&tzo=2"  # Mettez à jour l'URL si nécessaire
    driver.get(url)
    time.sleep(15)  # Attendez que la page se charge complètement
    start_time = time.time()
    try:
        with open("data_brute.txt", "w") as file:
            while time.time() - start_time < 120:  # Continue this loop for 15 seconds
                try:
                    # Attente explicite pour s'assurer que les éléments SVG sont chargés
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'svg'))
                    )
                    # Ciblez le texte par sa classe et ses attributs
                    text_selector = "text.crash-game__counter[font-size='83'][x='1160'][y='356']"
                    text_element = driver.find_element(By.CSS_SELECTOR, text_selector)
                    text_content = text_element.text
                    # Fetch text from the span element
                    span_selector_bets = "span.crash-total__value.crash-total__value--bets.crash-text"
                    span_element_bets = driver.find_element(By.CSS_SELECTOR, span_selector_bets)
                    span_content_bets = span_element_bets.text.strip()
                    # Fetch text from the span element
                    span_selector_prize = "span.crash-total__value.crash-total__value--prize.crash-text"
                    span_element_prize = driver.find_element(By.CSS_SELECTOR, span_selector_prize)
                    span_content_prize = span_element_prize.text.strip()
                    # Fetch text from the span element
                    span_selector_players = "span.crash-total__value.crash-total__value--players.crash-text"
                    span_element_players = driver.find_element(By.CSS_SELECTOR, span_selector_players)
                    span_content_players = span_element_players.text.strip()

                    if len(text_content)>0: 
                        file.write(' * value x : ' + text_content +
                                   ' * value--bets : '+ span_content_bets +
                                   ' * value--prize : ' + span_content_prize +
                                   ' * value--players : ' + span_content_players
                                   +" \n\n  ")  # Write data to file with a separator
                        time.sleep(0.5)
                        
                except Exception as e:
                    print("Error during data extraction loop:", e)
    except Exception as e:
        print("Error while writing to file:", e)
    finally:
        driver.quit()

def main():
    driver = setup()
    fetch(driver)

main()



