from math import e
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secret import USERNAME, PASSWORD, SERVER_ID

import json

PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])


driver = webdriver.Chrome(PATH, options = options)

driver.get("http://dash.townshiptale.com")


search = driver.find_element(By.ID, "username")
search.send_keys(USERNAME)

search = driver.find_element(By.ID, "password")
search.send_keys(PASSWORD)
search.send_keys(Keys.ENTER)

sleep(5)

driver.get("http://dash.townshiptale.com/servers/{}".format(SERVER_ID))

sleep(5)

#print(driver.current_url,'--------------------------')
#print(driver.page_source)

while True:
    sleep(3)
    search = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/div/input')
    
    player_name = "a player's name"

    search.send_keys("player detailed {}".format(player_name))
    search.send_keys(Keys.ENTER)
 
    sleep(3)
    
    #print(driver.page_source)
    
    search = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/p')
    
    print(search.text)
    
    
    player_json = json.loads(search.text)
    
    print("player {} is at chunk {}.".format(player_json['username'], player_json['Chunk']))