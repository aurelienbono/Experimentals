# import logging
# import pickle
# import os
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import urllib.parse

# # Configuration des logs
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI()

# class UnshortenRequest(BaseModel):
#     short_url: str
#     phone_number: str
#     password: str

# def save_cookies(driver, path):
#     with open(path, 'wb') as filehandler:
#         pickle.dump(driver.get_cookies(), filehandler)
#     logger.info("Cookies sauvegardés.")

# def load_cookies(driver, path):
#     with open(path, 'rb') as cookiesfile:
#         cookies = pickle.load(cookiesfile)
#         for cookie in cookies:
#             driver.add_cookie(cookie)
#     logger.info("Cookies chargés.")

# def unshorten_url_with_login(short_url: str, phone_number: str, password: str) -> str:
#     logger.info(f"Début du traitement pour l'URL : {short_url}")

#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Pour éviter d'ouvrir une fenêtre de navigateur
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--no-sandbox")
#     logger.info("Options du navigateur configurées.")

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     logger.info("Navigateur Chrome initialisé.")

#     cookie_path = 'facebook_cookies.pkl'

#     try:
#         if os.path.exists(cookie_path):
#             logger.info("Chargement des cookies de session.")
#             driver.get("https://www.facebook.com/")
#             load_cookies(driver, cookie_path)
#             driver.refresh()
#         else:
#             logger.info("Connexion manuelle requise pour sauvegarder les cookies.")
#             driver.get("https://www.facebook.com/")
#             time.sleep(3)

#             phone_input = driver.find_element(By.ID, "email")
#             password_input = driver.find_element(By.ID, "pass")

#             phone_input.send_keys(phone_number)
#             password_input.send_keys(password)
#             password_input.send_keys(Keys.RETURN)

#             time.sleep(5)
#             save_cookies(driver, cookie_path)

#         # Accéder directement à l'URL raccourcie après la connexion
#         logger.info(f"Accès à l'URL raccourcie : {short_url}")
#         driver.get(short_url)

#         # Attendre que la redirection se produise
#         time.sleep(30)

#         # Récupérer l'URL finale
#         expanded_url = driver.current_url
#         logger.info(f"URL finale récupérée : {expanded_url}")
#     except Exception as e:
#         logger.error(f"Erreur lors du traitement : {e}")
#         raise
#     finally:
#         driver.quit()
#         logger.info("Navigateur fermé.")

#     return expanded_url

# @app.post("/unshorten/")
# async def unshorten_url(request: UnshortenRequest):
#     try:
#         logger.info(f"Requête reçue avec URL : {request.short_url}")
#         expanded_url = unshorten_url_with_login(request.short_url, request.phone_number, request.password)
#         logger.info(f"URL étendue récupérée : {expanded_url}")
#         return {"expanded_url": expanded_url}
#     except Exception as e:
#         logger.error(f"Erreur interne : {e}")
#         raise HTTPException(status_code=500, detail=str(e))



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

    # Extraire le titre de la vidéo
    title_tag = soup.find('meta', property='og:title')
    if title_tag:
        video_title = title_tag.get('content')
        print(f"Titre de la vidéo : {video_title}")
    else:
        print("Impossible de trouver le titre de la vidéo.")
else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")
