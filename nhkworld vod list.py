from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
# import time
import pandas as pd
options = webdriver.FirefoxOptions()
# options.headless = True
driver = webdriver.Firefox(options=options)
url = r"https://www3.nhk.or.jp/nhkworld/en/vod/latest/"
driver.get(url)
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'nw_gdpr_confirm_button')))
element.click()
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'c-viewMore__btn')))
element.click()
# WebDriverWait(driver, 20)
raw = driver.page_source
driver.quit()
page = bs(raw, 'html5lib')
c_tiles = page.find('div', {'class', 'c-tiles'})
divs = c_tiles.find_all('div', {"class": "c-card "})
links = [div.find('a') for div in divs if div]
links_contents = [{'url': 'https://www3.nhk.or.jp' + link['href'],
                   'body': link.find('p').text,
                   'title': link.find('h3').text} for link in links]
frame = pd.DataFrame(links_contents, columns=['title', 'body', 'url'])
frame.to_csv('out.csv')
