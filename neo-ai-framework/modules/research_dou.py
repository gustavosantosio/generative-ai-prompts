from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import math


def search_the_directory_by_keywords():
    try:
        browser = webdriver.Edge()
        browser.get("https://www.in.gov.br/leiturajornal?secao=dou3")

        time.sleep(7)

        browser.maximize_window()
        browser.switch_to.window(browser.current_window_handle)
        advanced_search = browser.find_element(By.XPATH, '//*[@id="toggle-search-advanced"]')
        advanced_search.click()

        time.sleep(3)

        search_todays_date = browser.find_element(By.XPATH, '//*[@id="dia"]')
        time.sleep(3)
        search_todays_date.click()
        search_bar = browser.find_element(By.XPATH, '//*[@id="search-bar"]')
        search_bar.click()

        time.sleep(3)

        search_bar.send_keys('"Segurança da Informação"')

        time.sleep(3)

        search_bar.send_keys(Keys.ENTER)

        time.sleep(8)

        print('Function 01 OK')

    except OSError as err:
        print("OS error:", err)
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
