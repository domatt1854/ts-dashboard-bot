from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from secret import USERNAME, PASSWORD, SERVER_ID

import json

import pandas as pd
import re

from os.path import exists




class Quit:
    
    
    def __init__(self):
        '''
        init - initiates the web driver
        '''
    
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # change the PATH to where the chromedriver executable is stored
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

            # close and launch a new instance if auth failed

            self.driver.close()          
            sleep(3)
            self.__init__()




    def send_command(self, command):
        '''
        locates the command runner position in the dashboard and inputs the provided
        command into the command runner
        '''
        
        try:
            
            self.command_runner = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/form/div/div/input'))
            )
            
            # clear the command runner and send the command
            self.command_runner.clear()
            self.command_runner.send_keys(command)
            self.command_runner.send_keys(Keys.ENTER)

            print("successfully sent command \'{}\'".format(command))
            sleep(3)
            
            return 0
        
        except TimeoutException:
            self.auth()
    
    """
    This grabs the data outputted by certain commands. 
        xpath - the specific path to the data
    """

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

        try:
            # xpath is different when there is only one player,
            # it has no list number

            # no way of checking which case it is without refreshing the page
            # and checking how many players are active. 
            
            xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/li'


            player_data = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
            )
                
            player_list.append(json.loads(player_data.text))
        
        except Exception:
            pass

        try:
            
            for i in range(1, 9):
            
                xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/code/li[{}]'.format(i)
            
                
                player_data = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                )
                
                player_list.append(json.loads(player_data.text))
                    
        except TimeoutException:
            print("timeout exception on get_player_list_data at: {}".format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))

        except json.JSONDecodeError:
            print("json decode error on get_player_list_data at: {}".format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))

        except StaleElementReferenceException:
            print("stale element exception on get_player_list_data at: {}".format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))

    
        return player_list
        

    """
    get_num_players() uses the "X elements" text in the dashboard to grab how many players there are.
    This is an alternative to using the command runner because the command runner requires at least one player to be 
    in the server to be enabled.

    The main caveat is that this text will not be constantly updated. Users will have to use the 'player list' command 
    to see who is currently active on the server.

    """
    def get_num_players(self):
        
        try:
            xpath = '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[3]/div/div[1]/h3'
            

            search = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )


            result = search.text
            
            return int(result[0])


        except NoSuchElementException:
            return None
        except TimeoutException:
            return None
        except StaleElementReferenceException:
            return None
        
    """
    checks if usual username and password entries are available, if they are not, return 0
    else, log in as usual
    """
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
    
    # initialize the webdriver and login
    bot = Quit()
    bot.auth()
    
    # to track if the script is actually interacting with the command runner
    # I might want to replace this later with a simple URL check.
    login_attempt_count = 0

    # two ways of getting number of players, from the "X online" on the dashboard website
    # itself, or running 'player list' as a command. 

    # get_num_players() uses the 'X online' method, which only works after we immediately
    # refresh the page, else it will return an innaccurate value. 
    num_players = bot.get_num_players()

    print("Number players online: {}".format(num_players))

    # infinite for loop of logging.    
    while(True):

        # reset if we aren't on the correct page (the server page)
        if bot.driver.current_url != "http://dash.townshiptale.com/servers/{}".format(SERVER_ID):
            bot.auth()
            num_players = bot.get_num_players()

        
        # if we are able to get the number of players online
        # and there are some players in the server
        if(num_players and num_players != 0):
            
            # get the ID's and usernames of all players currently on the server
            bot.send_command("player list")
            
            player_list = bot.get_player_list_data()
            num_players = len(player_list)

            # get current time to mark item and player data
            now = datetime.now()
            
            
            if(num_players != 0):

                # reset our interaction counter because the 
                login_attempt_count = 0

                for i, player in enumerate(player_list):


                    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
                    current_day = now.strftime("%m.%d.%Y")


                    print(i, ": ", player['username'], "at", current_time)
                    
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

             
                        # create new files with headers
                        # if they do not exist yet

                        item_location_filename = 'data/{}_items.csv'.format(current_day)
                        location_filename = 'data/{}_bag_location.csv'.format(current_day)

                        if not exists(item_location_filename):
                            with open(item_location_filename, 'w') as f:
                                f.write("Index,Time,Username,Item,Location\n")
                            
                        if not exists(location_filename):
                            with open(location_filename, 'w') as f:
                                f.write('Index,Time,Username,Bag,Location\n')
                      
                        
                        
                        df.to_csv(item_location_filename, mode = 'a', header = False)
                        print("wrote to {}".format(item_location_filename))

                        df_bag.to_csv(location_filename, mode = 'a', header = False)
                        print("wrote to {}".format(location_filename))


                        

        # in the case where we are on the correct website
        # but there are no active players
        
        elif num_players is not None and num_players == 0:
            
            sleep(60)
            print("sleeping for a minute at {}".format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
            bot.refresh()

            num_players = bot.get_num_players()


        # not on the correct page, auto-logged out, else
        else:
            # tab this if it doesn't work later

            print(num_players is not None)
            print(num_players == 0)
            print(num_players)
            
            login_status = bot.check_login()
            
            if(login_status == 0):
                login_attempt_count += 1
            
                print("failed login check, current login attempt count: {}".format(login_attempt_count))
            
            if(login_attempt_count > 2):
                datetime_now = datetime.now()
                currtime = datetime_now.strftime("%m/%d/%Y %H:%M:%S")
                
                print("White screen! Reauthorizing at {}.....".format(currtime))
                
                bot.driver.close()          
                
                sleep(3)
                
                bot = Quit()

                bot.auth()

                num_players = bot.get_num_players()

                login_attempt_count = 0

            
    
                

if __name__ == "__main__":

    
    main()