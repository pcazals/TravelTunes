import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from app import create_playlist_for_trip

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
spotipy_token = os.environ.get('SPOTIPY_TOKEN')

with open("token.txt", "w") as fichier:
    fichier.write(spotipy_token)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, open_browser=False, cache_path="token.txt"))
print(sp.me()['id'])

def test_create_playlist_for_trip():
    duration_min = 60
    #Création d'une playliste avec create_playlist_for_trip()
    playlist = create_playlist_for_trip(duration_min, 'Ales', 'Montpelier', 'Pop')

    playlist_id = playlist[1]
    fields = 'tracks.items(track(duration_ms))'
    #List toutes les tracks dans la playlist qui vient d'être générée
    track_duration_ms = sp.playlist(playlist_id, fields)
    
    duration_ms = 0
    #Addition des timer de chaque tracks 
    for track in track_duration_ms['tracks']['items']:
        duration_ms += track['track']['duration_ms']
    
    #Calcul du pourcentage entre notre traget et le temps mesurée générrer par la fonction
    difference_percent = abs(((duration_ms / 1000) - (duration_min * 60)) / (duration_min * 60)) * 100

    #Suppression de la playslist du profile Spotify
    sp.user_playlist_unfollow(sp.me()['id'], playlist_id)
    #La différence doit être plus ou moins 10%
    assert difference_percent <= 10


"""
#delte all playlists
for playlist in sp.user_playlists(sp.me()['id'], limit=200)['items']:
    sp.user_playlist_unfollow(sp.me()['id'], playlist['id'])
"""
