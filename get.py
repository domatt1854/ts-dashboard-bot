import requests

from datetime import datetime




def get_server_status():
    
    url = "https://967phuchye.execute-api.ap-southeast-2.amazonaws.com/prod/api/servers/2004963217"

    querystring = {"limit":"20"}
    
    # insert your user agent here
    


    ## INSERT YOUR HEADERS HERE. GENERATE CODE FROM POSTMAN/INSOMNIA
    headers = {}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def main():
    
    while(True):
        sleep(60)
        players = get_server_status()
        
        now = datetime.now()

        with open('players.csv', 'a') as f:
            current_time = now.strftime("%H:%M:%S")

            for player in players['online_players']:
                f.write("{},{}\n".format(current_time, player['username']))
        
    
if __name__ == '__main__':
    main()
        
