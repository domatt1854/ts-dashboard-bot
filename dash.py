from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from secret import USERNAME, PASSWORD, SERVER_ID

import json

import pandas as pd
import re

import os

class Quit:
    
    
    def __init__(self):
        '''
        init - initiates the web driver
        '''
    
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        PATH = "C:\Program Files (x86)\chromedriver.exe"


        self.driver = webdriver.Chrome(PATH, options = options)

    def get(self, url, delay = 0):
        '''
        wrapper to navigate to a page and sleep if provided
        '''
        self.driver.get(url)
        
        if delay != 0:
            sleep(delay)
            

    def auth(self):
        '''
        logs to the dashboard website and enters in user credentials
        '''
        
        self.driver.get("http://dash.townshiptale.com")

        try:
            
            self.username = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            self.username.send_keys(USERNAME)
            
            self.password = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            
            self.password.send_keys(PASSWORD)
            self.password.send_keys(Keys.ENTER)
            
            sleep(3)
            
            self.driver.get("http://dash.townshiptale.com/servers/{}".format(SERVER_ID))
            
        except TimeoutException:
            self.driver.refresh()
            self.auth()



    def send_command(self, command):
        '''
        locates the command runner position in the dashboard and inputs the provided
        command into the command runner
        '''
        
        try:
            
            self.command_runner = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/div/input'))
            )
            
            self.command_runner.clear()
            self.command_runner.send_keys(command)
            self.command_runner.send_keys(Keys.ENTER)
            print("successfully sent command \'{}\'".format(command))
            sleep(3)
            
            return 0
        
        except TimeoutException:
            self.auth()
    
    def get_data(self, xpath):
        
        
        try:
            command_data = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
            )
            
            if command_data is not None and command_data.text is not None:

                return json.loads(command_data.text)
            else:
                return None
        
        except TimeoutException:
            return None
        except json.JSONDecodeError:
            return None
    
    def get_player_list_data(self):
        
        player_list = []
        
        for i in range(1, 9):
        
            xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/li[{}]'.format(i)
        
            try:
                player_data = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                )
                
                player_list.append(json.loads(player_data.text))
            
            except TimeoutException:
                return player_list
    
        return player_list
        

    def get_num_players(self):
        
        try:
            xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[1]/h3'
            
            search = self.driver.find_element(By.XPATH, xpath)
            
            result = search.text
            
            return result
        except NoSuchElementException:
            return None
        
    def check_login(self):
        
        try:
            username = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "password"))
            )

            username.send_keys(USERNAME)
            
            password.send_keys(PASSWORD)
            password.send_keys(Keys.ENTER)

            sleep(3)
            
            self.driver.get("http://dash.townshiptale.com/servers/{}".format(SERVER_ID))
            

            
            print("logged in")
            
        except TimeoutException:
            return 0
    
    def refresh(self):
        self.driver.refresh()
        
            

def main():
    

    
    seconds = 0
    
    bot = Quit()
    
    bot.auth()
    
    login_attempt_count = 0


    
    while(True):
        response = bot.get_num_players()
        
        
        if(response and '0' not in response):
            
            bot.send_command("player list")
            
            login_attempt_count = 0
                        
            data = bot.get_player_list_data()
            now = datetime.now()
            
            
            if(data):
                for i, player in enumerate(data):


                    current_time = now.strftime("%m/%d/%Y %H:%M:%S")


                    print(i, ": ", player['username'])
                    
                    bot.send_command('player inventory \"{}\"'.format(player['username']))
                    
                    
                    data = bot.get_data('//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/li')
                    
                    player_items = []
                    
                    
                    if data:
                        
                        bag = 'None'
                        
                        for i in data['All']:
                            
                            item = i['Name']
                            #print("appending ", item)
                            
                            
                            item_name = item.replace('(Clone)', '')
                            #print("after strip clonse", item_name)
                            item_name = item_name.replace('-' , '')
                           # print(item_name)
                            item_name = item_name.replace(' ', '')
                            #print(item_name)
                            result = re.sub(r"\d+", "", item_name)
                            #print("final: ", result)

                            if 'HoarderBag' in result:
                                bag = 'HoarderBag'
                            elif 'WoodenBag' in result:
                                bag = 'WoodenBag'
                            elif result == 'Bag':
                                bag = 'Bag'

                            
                            player_items.append(result)
                    
                    
                            #print(result)
                        
                        location_xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/p'
                        
                        bot.send_command("player detailed {}".format(player['username']))
                        
                        location_data = bot.get_data(location_xpath)
                        
                        if location_data:
                            location_data = location_data['Chunk']
                            location_data = location_data.strip('(Alta.Chunks.LocationChunk)')
                        else:
                            location_data = "None"
                            
                        df_dict = {
                            'Time': current_time,
                            'Username': player['username'],
                            'Items': player_items,
                            'Location': location_data
                        }
                        
                        df_dict_bag_only = {
                            'Time': [current_time],
                            'Username': [player['username']],
                            'Bag': [bag],
                            'Location': [location_data]
                        }
                        
                        
                        #print("player items: ", player_items)
                        
                        df = pd.DataFrame(df_dict)
                        df_bag = pd.DataFrame(df_dict_bag_only)
                        
                        df.to_csv('3.7.22.csv', mode = 'a', header = False)
                        df_bag.to_csv('3.7.22_bag_location.csv', mode = 'a', header = False)
                        
                        print("wrote to item_locations.csv")
                        
                            
                        # line 381
                    
  
        # tab this if it doesn't work later
        #print("checking login", seconds)
        login_status = bot.check_login()
        
        if(login_status == 0):
            login_attempt_count += 1
            
        
        if(login_attempt_count > 10):
            datetime_now = datetime.now()
            currtime = datetime_now.strftime("%m/%d/%Y %H:%M:%S")
            
            print("White screen! Reauthorizing at {}.....".format(currtime))
            
            bot.driver.close()          
            
            sleep(3)
            
            bot = Quit()

            bot.auth()
        

            #
                # datetime object containing current date and time
                # now = datetime.now()
                
                # print("now =", now)

                # # dd/mm/YY H:M:S
                # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                # print("date and time =", dt_string)

                
                # Index,Time,Username,Bag,Location
                # Index,Time,Username,Item,Location
                

if __name__ == "__main__":
    
    print(os.getcwd())
    
    main()