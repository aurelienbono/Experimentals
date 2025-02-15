import requests
from bs4 import BeautifulSoup

# URL de la page fb.watch
url = "https://fb.watch/xMmvFNnx0x/"

# Envoyer une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Analyser le contenu HTML de la page avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraire l'URL normale de la vidéo
    meta_tag = soup.find('meta', property='og:video')
    if meta_tag:
        video_url = meta_tag.get('content')
        print(f"URL normale de la vidéo : {video_url}")
    else:
        print("Impossible de trouver l'URL normale de la vidéo.")
else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")
