import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIFY_ID = os.environ['SPOTIFY_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']

# WEB SCRAPE of BILLBOARD TOP 100 songs
date = input("Which year do you want to travel to? Enter date as YYYY-MM-DD: ")
year = date.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
top_100_songs = [song.getText().strip() for song in soup.select("li ul li h3")]


# SPOTIFY API CALL TO GET URIs and CREATE PLAYLIST and ADD SONGS
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))

user_id = sp.current_user()['id']

# get song uri
song_uri_list = []
for song in top_100_songs:
    song_info = sp.search(f"track: {song} year: {year}", type="track")
    try:
        uri = song_info['tracks']['items'][0]['uri']
        song_uri_list.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create playlist
my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"{date} Billboard Top Tracks", public=False)

# add songs
sp.playlist_add_items(playlist_id=my_playlist['id'], items=song_uri_list)
