from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime 
import datetime as dt
import pytz
import time

class WebScraper:
    def __init__(self, driver_path, duration=120):
        """
        Initialise l'instance du WebScraper.

        Args:
            driver_path (str): Chemin vers le driver de Chrome.
        """
        self.driver_path = driver_path
        self.driver = None
        self.duration = duration

    def setup_driver(self):
        """
        Configure le navigateur pour le scraping avec Selenium.
        """
        print("----- Setting Up -----")
        service = Service(self.driver_path)
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=service, options=options)

    def fetch_data(self, url):
        """
        Extrait les données du site Web spécifié et les stocke dans un fichier CSV.

        Args:
            url (str): URL de la page à scraper.
        """
        print("----- Fetching Data -----")
        self.driver.get(url)
        time.sleep(5)  # Wait for the page to load completely
        start_time = time.time()
        try:
            with open(self.get_name_file(), "w", encoding='utf-8') as file:
                file.write("Timestamp,Value X,Value Bets,Value Prize,Value Players\n")
                while time.time() - start_time < self.duration:
                    try:
                        WebDriverWait(self.driver, 30).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, 'svg'))
                        )
                        data = self.extract_data()
                        if data['Value X'] == "":
                            time.sleep(5)
                        else :
                            timestamp = self.get_timestamp()
                            file.write(f"{timestamp},{data['Value X'].replace('x','')},{data['Value Bets']},{data['Value Prize']},{data['Value Players']}\n")
                    except Exception as e:
                        print(f"Error during data extraction loop: {e}")
        except Exception as e:
            print(f"Error while writing to file: {e}")
        finally:
            self.driver.quit()

    def extract_data(self):
        """
        Extracts required data from the web elements on the page.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        elements = {
            "Value X": "text.crash-game__counter[font-size='83'][x='1160'][y='356']",
            "Value Bets": "span.crash-total__value.crash-total__value--bets.crash-text",
            "Value Prize": "span.crash-total__value.crash-total__value--prize.crash-text",
            "Value Players": "span.crash-total__value.crash-total__value--players.crash-text"
        }
        data = {}
        for key, selector in elements.items():
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            data[key] = element.text.strip()
        return data

    def get_timestamp(self):
        """
        Returns the current time formatted as a string, adjusted to Morocco time.

        Returns:
            str: The formatted timestamp.
        """
        morocco_time = datetime.now(pytz.timezone('Africa/Casablanca'))
        return morocco_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_name_file(self):
        """
        Returns the name file of csv, with start and finish time.

        Returns:
            str: The formatted timestamp.
        """
        morocco_time = datetime.now(pytz.timezone('Africa/Casablanca'))
        return f"data_brute_{self.get_timestamp()}_to_{(morocco_time + dt.timedelta(seconds=self.duration)).strftime('%Y-%m-%d %H:%M:%S')}.csv"

# def main():
#     scraper = WebScraper(r'C:\Users\YasserAITLAZIZ\Downloads\chromedriver-win64\chromedriver.exe')
#     scraper.setup_driver()
#     url = "https://1xbet.ng/games-frame/games/371?co=85&cu=81&lg=en&wh=50&tzo=2"
#     scraper.fetch_data(url)

# if __name__ == "__main__":
#     main()
