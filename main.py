import requests
import string
import random
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date = input("Which year do you want to travel to? Type date in format YYYY-MM-DD:\n")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
web_html = response.text
soup = BeautifulSoup(web_html, "html.parser")

titles = soup.find_all(name="h3", class_="a-no-trucate")
artists = soup.find_all(name="span", class_="a-no-trucate")

titles_list = []
artists_list = []

for title in titles:
    new_title = title.getText().strip()
    titles_list.append(new_title)

for artist in artists:
    new_artist = artist.getText().strip()
    artists_list.append(new_artist)

# ----------------------------- AUTHORIZATION------------------------------------#

OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

REDIRECT_URL = os.environ["REDIRECT_URL"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

state = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
scope = "playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        state=state,
        scope=scope,
        cache_path="token.txt"
        )
)

user_id = sp.current_user()["id"]
print(user_id)

# ------------------------------ LIST OF SPOTIPY URI ----------------------------- #

song_uris = []
year = date.split("-")[0]

for index in range(0,100):
    result = sp.search(q=f"track:{titles_list[index]} year:{year}", type="track", limit=2)
    try:
        song_uri = result["tracks"]["items"][0]["uri"]
    except IndexError:
        pass
    else:
        song_uris.append(song_uri)

# ------------------------------- CREATE PLAYLIST -------------------------------- #

playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)["id"]

# ------------------------------- ADD SONGS TO PLAYLIST -------------------------- #

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)