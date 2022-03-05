from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException



from credentials import USERNAME, PASSWORD

from bs4 import BeautifulSoup

import requests

from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(PATH, options = options)

driver.get("https://dash.townshiptale.com/")
sleep(3)

search = driver.find_element(By.ID, "username")
search.send_keys(USERNAME)

search = driver.find_element(By.ID, "password")
search.send_keys(PASSWORD)
search.send_keys(Keys.ENTER)

sleep(5)

while True:

    try:
        driver.get("http://dash.townshiptale.com/servers/{}".format("2004963217"))
        
        search = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/div/input')
        search.send_keys("quit")
        search.send_keys(Keys.ENTER)
        sleep(5)

    except NoSuchElementException:
        
        driver.refresh()
        sleep(5)


