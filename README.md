# TravelTunes
![alt text](https://github.com/pcazals/traveltunes/blob/main/ressource/logo.jpg)

TravelTunes est une application innovante qui combine le calcul de temps de trajet via l'API de Waze avec la création d'une playlist personnalisée sur ![image]({https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white}), correspondant à la durée de votre trajet. Que vous soyez en route pour le travail, en voyage, ou simplement en quête d'une expérience musicale sur mesure pendant vos déplacements, TravelTunes est là pour enrichir chaque trajet.

## Fonctionnement

TravelTunes interroge l'API de Waze pour déterminer le temps de trajet entre deux points, puis utilise l'API de ![image]({https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white}) pour générer une playlist qui correspond exactement à la durée du trajet. Cette playlist est personnalisée en fonction de vos préférences musicales, vous offrant ainsi une expérience sur mesure.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé Docker sur votre machine. Vous aurez également besoin d'un compte Spotify et d'accéder à [Dashboard Spotify](https://developer.spotify.com/dashboard/) pour créer une application et obtenir vos clés d'API nécessaires.

## Configuration

1. Rendez-vous sur [Dashboard Spotify](https://developer.spotify.com/dashboard/).
2. Créez une nouvelle application pour obtenir votre `SPOTIPY_CLIENT_ID` et `SPOTIPY_CLIENT_SECRET`.
![alt text](https://github.com/pcazals/traveltunes/blob/main/ressource/createapp.png)
![alt text](https://github.com/pcazals/traveltunes/blob/main/ressource/basicinfo.png)

3. Notez l'URI de redirection que vous avez configurée pour votre application dans le Dashboard Spotify, cela sera votre `SPOTIPY_REDIRECT_URI`.
4. Si nécessaire, obtenez un `SPOTIPY_TOKEN` en suivant la documentation ci dessous.
5. Une fois les valeurs récupérées, il suffit de les intégrer dans votre environnement avec la commande ``export <token>``

### Création du SPOTIPY_TOKEN
- Se rendre dans le fichier ``app.py`` modifier la Ligne 18 et enlever 
``e, cache_path="token.txt"``

- Lancer le script app.py avec ``python3 app.py``
![alt text](https://github.com/pcazals/traveltunes/blob/main/ressource/script1.png)
Ouvrir le lien générer en console et se connecter avec spotify et autoriser l'accès. 

- Une fois la redirection efféctuée, copier le lien dans la console
![alt text](https://github.com/pcazals/traveltunes/blob/main/ressource/script2.png)

- le fichier .cache vient d'être généré
![alt text](https://github.com/pcazals/traveltunes/blob/main/ressource/script3.png)

- Copier sont contenu dans la varibale d'env SPOTIPY_TOKEN 

## Installation

Ouvrez un terminal et suivez ces étapes pour construire et exécuter le conteneur Docker de TravelTunes :

1. Clonez le dépôt ou téléchargez l'application TravelTunes : 
``git clone https://github.com/pcazals/TravelTunes)`` 
``cd TravelTunes``
2. Construisez l'image Docker :
``docker build -t TravelTunes:latest .``
3. Lancez le conteneur Docker :
``docker run -d -e SPOTIPY_CLIENT_SECRET=<VotreSecretClient> -e SPOTIPY_CLIENT_ID=<VotreClientId> -e SPOTIPY_REDIRECT_URI=<VotreURIdeRedirection> -e SPOTIPY_TOKEN=<VotreToken> -p 5000:5000 TravelTuness:latest``

Remplacez, `<VotreSecretClient>`, `<VotreClientId>`, `<VotreURIdeRedirection>`, et `<VotreToken>` par vos informations de dépôt et Spotify personnelles.

## Auteurs

* **Paul CAZALS** _alias_ [@pcazals](https://github.com/pcazals)het(upso`h)