from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from credentials import USERNAME, PASSWORD

from bs4 import BeautifulSoup

import requests

from time import sleep

PATH = "C:\Program Files (x86)\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(PATH, options = options)

driver.get("https://dash.townshiptale.com/")

search = driver.find_element(By.ID, "username")
search.send_keys(USERNAME)

search = driver.find_element(By.ID, "password")
search.send_keys(PASSWORD)
search.send_keys(Keys.ENTER)

sleep(5)



player_detail = "curl \"https://967phuchye.execute-api.ap-southeast-2.amazonaws.com/prod/api/servers/2004963217?limit=20\" ^-H \"authority: 967phuchye.execute-api.ap-southeast-2.amazonaws.com\" ^-H \"sec-ch-ua: ^\\^\" Not A;Brand^\\^\";v=^\\^\"99^\\^\", ^\\^\"Chromium^\\^\";v=^\\^\"98^\\^\", ^\\^\"Google Chrome^\\^\";v=^\\^\"98^\\^\"\" ^-H \"authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiIxMzkyMjAxMDI4IiwiVXNlcm5hbWUiOiJtYXR0aGV3ZG8iLCJyb2xlIjoiQWNjZXNzIiwiaXNfdmVyaWZpZWQiOiJ0cnVlIiwiUG9saWN5IjpbImdhbWVfYWNjZXNzX3B1YmxpYyIsInNlcnZlcl9hY2Nlc3NfdHV0b3JpYWwiLCJzZXJ2ZXJfYWNjZXNzX29jdWx1c19vdmVyd29ybGQiLCJzZXJ2ZXJfYWNjZXNzX29jdWx1c190dXRvcmlhbCJdLCJleHAiOjE2NDY0NDg2ODcsImlzcyI6IkFsdGFXZWJBUEkiLCJhdWQiOiJBbHRhQ2xpZW50In0.djSUKmIvDBsQy-iuDKObdQc2AhLu295P1jSjsDSbMnc\" ^-H \"content-type: application/json\" ^-H \"sec-ch-ua-mobile: ?0\" ^-H \"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36\" ^-H \"x-api-key: 2l6aQGoNes8EHb94qMhqQ5m2iaiOM9666oDTPORf\" ^-H \"sec-ch-ua-platform: ^\\^\"Windows^\\^\"\" ^-H \"accept: */*\" ^-H \"origin: http://dash.townshiptale.com\" ^-H \"sec-fetch-site: cross-site\" ^-H \"sec-fetch-mode: cors\" ^-H \"sec-fetch-dest: empty\" ^-H \"referer: http://dash.townshiptale.com/\" ^-H \"accept-language: en-US,en;q=0.9\" ^--compressed"

response = requests.request("GET", player_detail)

print(response.text)


print(driver.page_source)

#response = requests.get("https://dash.townshiptale.com/servers/2004963217")

#print("-----------------------")

# soup = BeautifulSoup(
#     response.text,
#     'html.parser'
# )

# print(response.text)


while(True):
    pass