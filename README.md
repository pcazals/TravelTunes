# TravelTunes

TravelTunes est une application innovante qui combine le calcul de temps de trajet via l'API de Waze avec la création d'une playlist personnalisée sur Spotify, correspondant à la durée de votre trajet. Que vous soyez en route pour le travail, en voyage, ou simplement en quête d'une expérience musicale sur mesure pendant vos déplacements, TravelTunes est là pour enrichir chaque trajet.

## Fonctionnement

TravelTunes interroge l'API de Waze pour déterminer le temps de trajet entre deux points, puis utilise l'API de Spotify pour générer une playlist qui correspond exactement à la durée du trajet. Cette playlist est personnalisée en fonction de vos préférences musicales, vous offrant ainsi une expérience sur mesure.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé Docker sur votre machine. Vous aurez également besoin d'un compte Spotify et d'accéder à [Dashboard Spotify](https://developer.spotify.com/dashboard/) pour créer une application et obtenir vos clés d'API nécessaires.

## Configuration

1. Rendez-vous sur [Dashboard Spotify](https://developer.spotify.com/dashboard/).
2. Créez une nouvelle application pour obtenir votre `SPOTIPY_CLIENT_ID` et `SPOTIPY_CLIENT_SECRET`.
3. Notez l'URI de redirection que vous avez configurée pour votre application dans le Dashboard Spotify, cela sera votre `SPOTIPY_REDIRECT_URI`.
4. Si nécessaire, obtenez un `SPOTIPY_TOKEN` en suivant la documentation de l'API Spotify.

## Installation

Ouvrez un terminal et suivez ces étapes pour construire et exécuter le conteneur Docker de TravelTunes :

1. Clonez le dépôt ou téléchargez l'application TravelTunes : 
``git clone https://github.com/pcazals/TravelTunes)`` 
``cd TravelTunes``
2. Construisez l'image Docker :
``docker build -t TravelTunes:latest .``
3. Lancez le conteneur Docker :
``docker run -d -e SPOTIPY_CLIENT_SECRET=<VotreSecretClient> -e SPOTIPY_CLIENT_ID=<VotreClientId> -e SPOTIPY_REDIRECT_URI=<VotreURIdeRedirection> -e SPOTIPY_TOKEN=<VotreToken> -p 5000:5000 TravelTuness:latest``

Remplacez `<URLDuDépôt>`, `<VotreSecretClient>`, `<VotreClientId>`, `<VotreURIdeRedirection>`, et `<VotreToken>` par vos informations de dépôt et Spotify personnelles.

## Auteurs

* **Paul CAZALS** _alias_ [@pcazals](https://github.com/pcazals)het(upso`h)