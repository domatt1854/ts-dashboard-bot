from math import e
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secret import USERNAME, PASSWORD, SERVER_ID, HEADERS
import json
import requests

PATH = "C:\Program Files (x86)\chromedriver.exe"

class TownshipLogger():
    def __init__(self):
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(PATH, options = options)        
        self.player_list = []
        
    def ping_server(self):
        
        url = "https://967phuchye.execute-api.ap-southeast-2.amazonaws.com/prod/api/servers/2004963217"
    
        try:
            response = requests.request("GET", url, headers=HEADERS, params={"limit":"20"})
            
            if(response.status_code == 200):
                return response.json()
        
        except e:
            print(e)
            return None
        
    def authenticate(self):

        self.driver.get("http://dash.townshiptale.com")

        self.search = self.driver.find_element(By.ID, "username")
        self.search.send_keys(USERNAME)

        self.search = self.driver.find_element(By.ID, "password")
        self.search.send_keys(PASSWORD)
        self.search.send_keys(Keys.ENTER)

    def set_command_runner(self):
        
        self.driver.get("http://dash.townshiptale.com/servers/{}".format(SERVER_ID))
        
        command_runner_xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/div/input'
        try:
            self.command_runner = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, command_runner_xpath))
            )
        except e:
            print(e)


    def get_player_detail(self, username):
        player_detail_json_xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/p'
        
        if self.command_runner:
            self.command_runner.send_keys("player detailed {}".format(username))
            self.command_runner.send_keys(Keys.ENTER)
            
            try:
                player_json = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, player_detail_json_xpath))
                )
            except e:
                print(e)
                return None
                
            return json.loads(player_json.text)

    def write_to_csv(self, data, params, file):
        
        if('.csv' not in file[-4]):
            return
        
        with open(file, 'r') as f:
            
            headers = next(f)
            


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
    
    
    
def main():
    
    print("asd")
    
if __name__ == '__main__':
    main()