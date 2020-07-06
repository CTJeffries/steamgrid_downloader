# download_animated_grids.py

import requests
import urllib.request
import os

def download_animated_grids(steam_api_key, steam_id, steam_grid_api_key):
    # Get list of games
    response = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json".format(steam_api_key, steam_id))
    if response:
        games = response.json()['response']['games']
        games = [x['appid'] for x in games]
    else:
        print("Unable to find user games, check Steam ID and Steam API Key")
        exit(-1)

    # Get list of grid urls
    urls = []
    for game in games:

        response =  requests.get('https://www.steamgriddb.com/api/v2/grids/steam/{0}'.format(game), 
                                headers={'Authorization': 'Bearer {0}'.format(steam_grid_api_key)}, 
                                params={'styles': ['alternate'], 'dimensions': ['600x900'], 'types': ['animated']})

        if response:
            data = response.json()['data']
            for grid in data:
                if not grid['nsfw']:
                    urls.append((grid['url'], game))
                    break
        else:
            print("No animated grids for {0}, skipping...".format(game))

    # Download images into a folder
    try:
        os.mkdir("SteamGrids")
    except FileExistsError:
        pass
    except:
        print("Unable to create directpory.")
        exit(-1)
    for url in urls:
        #urllib.request.urlretrieve(url[0], "SteamGrids/{0}p.png".format(url[1]))
        with open("SteamGrids/{0}p.png".format(url[1]), "wb") as f:
            f.write(requests.get(url[0]).content)
    

if __name__ == '__main__':
    # Put your Steam API key here
    steam_api_key = '<YOUR KEY HERE>'

    # Put your Steam ID here
    steam_id = '<YOUR ID HERE>' 
    
    # Put your Steam Grid DB API key here
    steam_grid_api_key = '<YOUR KEY HERE>'

    download_animated_grids(steam_api_key, steam_id, steam_grid_api_key)
