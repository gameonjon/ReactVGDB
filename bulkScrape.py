import os
import requests
import mysql.connector
from bs4 import BeautifulSoup

#DB connection
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Mysq1",
    "database": "vgdb"
}

#IGDB Credentials
CLIENT_ID = "s44b4e3nlu0w6tw9ibrh3v0qjbcmde"
CLIENT_SECRET = "7y5boh2c9p2rwp4iddy7grw5em7c5p" #replace after ~60 days

#Get OAuth Token
def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params)
    response_data = response.json()

    access_token = response_data.get("access_token")
    print(f"{access_token}")
    return access_token

#path to images folder
image_folder = "./public/images"
os.makedirs(image_folder, exist_ok=True) #ensure directory exists

#connect ot DB and fetch all games
def get_game_list():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT g_title FROM Games")
        games = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return games
    except mysql.connector.Error as err:
        print(f"ERROR: {err}")
        return []
    
#download and save images
def save_image(image_url, image_name):
    try: 
        response = requests.get(image_url, timeout=5)
        response.raise_for_status() # raise exception for http errors
        with open(os.path.join(image_folder, image_name), "wb") as file:
            file.write(response.content)
        print(f"Saved: {image_name}")
    except requests.RequestException as e:
        print(f"Failed to download {image_name}: {e}")

#scrape game images
def download_game_image(game_name, access_token):

    searchUrl = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json" #ensure response is JSON
        }
    game_name = game_name.replace(":", "")
    query = f'search "{game_name}"; fields id, name, cover; limit 1;'

    response = requests.post(searchUrl, headers=headers, data=query)

    try:
        response.raise_for_status()
        data = response.json()
        # print(f"{data}")
        if data and "cover" in data[0]:
            cover_id = data[0]["cover"]
            cover_url = get_cover_url(cover_id, access_token)

            if cover_url:
                save_image(cover_url, f"{game_name.replace(' ', '_')}.jpg")
            else:
                print(f"Cover not found for {game_name}")
        else:
            print(f"No image found for {game_name}")

    except requests.RequestException as e:
        print(f"Failed to fetch results for {game_name}: {e}")

#get cover image url
def get_cover_url(cover_id, access_token):
    cover_url = "https://api.igdb.com/v4/covers"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json" #ensure response is JSON
    }
    query = f'fields url; where id = {cover_id};'

    response = requests.post(cover_url, headers=headers, data=query)

    try:
        response.raise_for_status()
        data = response.json()

        if data:
            return f"https:{data[0]['url'].replace('t_thumb', 't_cover_big')}"

    except requests.RequestException as e:
        print(f"Failed to fetch cover image: {e}")

    return None

#Run bulk scraper
if __name__ == "__main__":
    access_token = get_access_token()
    if not access_token:
        print("Failed to retrieve access token.")
    else:
        game_list = get_game_list()
        if not game_list:
            print("No games found in the database.")
        else:
            print(f"scraping images for {len(game_list)} games...")
            for game in game_list:
                download_game_image(game, access_token)