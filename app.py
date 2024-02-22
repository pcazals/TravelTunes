from flask import Flask, request, render_template
import WazeRouteCalculator
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import random

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

print('client scret :', client_secret)

# Initialisez Spotipy avec l'authentification utilisateur
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, open_browser=False, cache_path="token.txt"))
print(sp.me()['id'])
def create_playlist_for_trip(duration_minutes, start_addr, end_addr, genres):
    remaining_duration = duration_minutes * 60
    playlist_tracks = []
    while remaining_duration > 0:
        # Rechercher des chansons aléatoires
        results = sp.search(q=f"genre:{genres}", type='track', limit=10, offset=random.randint(0, 100))
        tracks = results['tracks']['items']

        # Sélectionner une chanson aléatoire
        track = random.choice(tracks)

        # Ajouter la chanson à la liste de lecture si sa durée ne dépasse pas la durée restante
        playlist_tracks.append(track['id'])
        remaining_duration -= track['duration_ms'] / 1000

    if not playlist_tracks:
        print("Aucune piste trouvée.")
        return
    
    # Création de la playlist
    playlist = sp.user_playlist_create(sp.me()['id'], name=f"Playlist '{start_addr}' '{end_addr}'Trajet Enfant", public=True)
    for i in range(0, len(playlist_tracks), 100):
        sp.playlist_add_items(playlist_id=playlist['id'], items=playlist_tracks[i:i+100])

    print(f"Playlist {playlist['name']} créée avec succès de {duration_minutes}min.")
    return playlist['external_urls']['spotify']

app = Flask(__name__)

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_address = request.form['start_address']  
        end_address = request.form['end_address']
        start_lat = request.form['start_lat']
        start_lng = request.form['start_lng']
        end_lat = request.form['end_lat']
        end_lng = request.form['end_lng']
        avoid_tolls = 'avoid_tolls' in request.form
        region = 'EU'
        try:
            route = WazeRouteCalculator.WazeRouteCalculator(
                f"{start_lat},{start_lng}",
                f"{end_lat},{end_lng}",
                region,
                avoid_toll_roads=avoid_tolls
            )
            route_info = route.calc_route_info()
            if route_info[0] >= 60:
                hours = int(route_info[0] / 60)
                minutes = int(route_info[0] % 60)
                result = f"De {start_address} à {end_address}, durée estimée: {hours}h{minutes:02d}, Distance: {route_info[1]} km"
            else:
                result = f"De {start_address} à {end_address}, durée estimée: {route_info[0]} minutes, Distance: {route_info[1]} km"

            if 'create_spotify_playlist' in request.form:
                selected_genres = request.form.getlist('genres')
                print(selected_genres)
                link_spotify = create_playlist_for_trip(int(route_info[0]), start_address, end_address, selected_genres)
                return render_template('index.html', result=result, link_spotify=link_spotify)
        except Exception as e:
            result = f"Erreur: {str(e)}"

        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
