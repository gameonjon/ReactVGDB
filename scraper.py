import sys
import os
import requests
from bs4 import BeautifulSoup

#function to download game image
def download_game_image(game_name):
    
    search_url = f"https://www.google.com/search?q={game_name.replace(' ', '+')}" 
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    #find the first image 
        #(modify this selector base on the website being scrapped)
    img_tag = soup.find("img")
    if not img_tag:
        print(f"No image found for {game_name}")
        return
    
    img_url = img_tag["src"]

    #create directory if it doesn't exist
    os.makedirs("images", exist_ok=True)

    #Download and save image
    img_data = requests.get(img_url).content
    image_path = f"images/{game_name.replace(' ','_')}.jpg"
    with open(image_path, "wb") as img_file:
        img_file.write(img_data)

    print(f"Downloaded {image_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper.py <game_name>")
    else:
        game_name = sys.argv[1]
        download_game_image(game_name)