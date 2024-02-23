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

# Création du fichier token.txt utilisé par SpotifyOAuth()
spotipy_token = os.environ.get('SPOTIPY_TOKEN')
with open("token.txt", "w") as fichier:
    fichier.write(spotipy_token)

# Initialisez Spotipy avec l'authentification utilisateur
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, open_browser=False, cache_path="token.txt"))
print(sp.me()['id'])


def create_playlist_for_trip(duration_minutes, start_addr, end_addr, genres):
    remaining_duration = duration_minutes * 60
    playlist_tracks = []
    index = 0
    # Ajout des tracks dans la liste playlist_tracks
    while remaining_duration > 0:
        # Rechercher des chansons aléatoires
        results = sp.search(q=f"genre:{genres[index]}", type='track', limit=10, offset=random.randint(0, 100))
        tracks = results['tracks']['items']
        # Changement de genre si il y en a plusieurs
        index = (index + 1) % len(genres)

        # Sélectionner une chanson aléatoire sur les 10 tracks renvoyés par spotify
        track = random.choice(tracks)

        # Si la tracks séléctionner est plus longue que 350s que notre traget on choisi une autre traget
        if remaining_duration - (track['duration_ms'] / 1000) < -350:
            continue

        # Ajouter la chanson à la liste de lecture si sa durée ne dépasse pas la durée restante
        playlist_tracks.append(track['id'])
        remaining_duration -= track['duration_ms'] / 1000

    if not playlist_tracks:
        print("Aucune piste trouvée.")
        return
    
    # Création de la playlist
    playlist = sp.user_playlist_create(sp.me()['id'], name=f"Playlist {' '.join(genres)} : '{start_addr}' '{end_addr}'", public=True)
    # Ajout par bloque de 100 (limitation Spotify) les tracks
    for i in range(0, len(playlist_tracks), 100):
        sp.playlist_add_items(playlist_id=playlist['id'], items=playlist_tracks[i:i+100])

    print(f"Playlist {playlist['name']} créée avec succès de {duration_minutes}min.")
    return [playlist['external_urls']['spotify'], playlist['id']]



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
                link_spotify = create_playlist_for_trip(int(route_info[0]), start_address, end_address, selected_genres)[0]
                return render_template('index.html', result=result, link_spotify=link_spotify, selected_genres=' '.join(selected_genres))
        except Exception as e:
            result = f"Erreur: {str(e)}"

        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)