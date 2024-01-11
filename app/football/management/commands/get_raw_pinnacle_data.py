
from django.core.management.base import BaseCommand
# import pandas as pd
import datetime
from football.models import PinnacleData

# from webdriver_manager.chrome import ChromeDriverManager

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
 

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
        
from selenium import webdriver
from selenium.webdriver.common.by import By

# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')


def get_betting_data(link, driver):

    data = []
    driver.get(link)

    for e in driver.find_elements(By.CLASS_NAME,'style_showAllButton__NW6iu'):
        e.click()
    
    for e in driver.find_elements(By.CLASS_NAME,'style_toggleMarketsText__2X9Do'):
        e.click()

    for e in driver.find_elements(By.XPATH,"//div[@data-test-id='Collapse']"):
        print("one collapse element found")
        print(e.text)
        data += [e.text]
        
    return data

def remove_periods(string):
    temp = string.split(".")
    replacement = ""
    for t in temp:
        replacement += t
    return replacement

def process_betting_data(betting_data):
    all_betting_data = {}
    for line in betting_data:
        info = line.split('\n')
        print(info)
        bet_type = info[0]
        bet_data = []
        for i in range(len(info)):
            if remove_periods(info[i]).isnumeric():
                bet_data += [{info[i-1]: info[i]}]
        all_betting_data[bet_type] = bet_data
    return all_betting_data

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        all_links = []
        games = []

        driver = webdriver.Chrome()
        driver.implicitly_wait(15)
        driver.get('https://www.pinnacle.com/en/football/matchups/')

        elems = driver.find_elements(By.XPATH,"//a[@href]")
        for elem in elems:
            all_links += [elem.get_attribute("href")]
        for link in all_links:
            print(link)
            if "https://www.pinnacle.com/en/football/nfl/" in link:
                print("is NFL")
                last_slug = link.split("/")[-2]
                if last_slug.isnumeric():
                    print("is numeric")
                    if link not in games:
                        print("not found, adding")
                        games += [link]
        # games
        all_betting_data = {}
        for game in games:
            raw_data = get_betting_data(game, driver)
            processed_data = process_betting_data(raw_data)
            all_betting_data[game] = processed_data
        new_pd_blob = PinnacleData(
            created=datetime.datetime.now(),
            data=all_betting_data
        )
        new_pd_blob.save()