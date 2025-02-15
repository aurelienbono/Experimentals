import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class UnshortenRequest(BaseModel):
    short_url: str
    phone_number: str
    password: str

def unshorten_url_with_login(short_url: str, phone_number: str, password: str) -> str:
    logger.info(f"Début du traitement pour l'URL : {short_url}")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Pour éviter d'ouvrir une fenêtre de navigateur
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    logger.info("Options du navigateur configurées.")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    logger.info("Navigateur Chrome initialisé.")

    try:
        # Encoder l'URL de la vidéo pour l'utiliser dans l'URL de Facebook
        encoded_video_url = urllib.parse.quote(short_url, safe='')
        logger.info(f"URL encodée : {encoded_video_url}")

        # Accéder à Facebook et se connecter avec l'URL de redirection
        logger.info(f"Accès à Facebook avec redirection vers : {short_url}")
        driver.get(f"https://www.facebook.com/login/?next={encoded_video_url}")
        logger.info("Page de connexion Facebook chargée.")

        # Attendre que la page de connexion s'affiche
        time.sleep(3)
        logger.info("Attente terminée après le chargement de la page de connexion.")

        # Remplir les informations de connexion
        phone_input = driver.find_element(By.ID, "email")  # ID du champ email (modifié si nécessaire)
        password_input = driver.find_element(By.ID, "pass")  # ID du champ mot de passe (modifié si nécessaire)
        logger.info("Champs de saisie pour email et mot de passe localisés.")

        phone_input.send_keys(phone_number)
        logger.info("Numéro de téléphone saisi.")
        password_input.send_keys(password)
        logger.info("Mot de passe saisi.")

        # Soumettre le formulaire
        password_input.send_keys(Keys.RETURN)
        logger.info("Formulaire de connexion soumis.")

        # Attendre la redirection après la connexion
        time.sleep(5)
        logger.info("Attente terminée après la soumission du formulaire.")

        # Récupérer l'URL finale
        expanded_url = driver.current_url
        logger.info(f"URL finale récupérée : {expanded_url}")
    except Exception as e:
        logger.error(f"Erreur lors du traitement : {e}")
        raise
    finally:
        driver.quit()
        logger.info("Navigateur fermé.")

    return expanded_url

@app.post("/unshorten/")
async def unshorten_url(request: UnshortenRequest):
    try:
        logger.info(f"Requête reçue avec URL : {request.short_url}")
        expanded_url = unshorten_url_with_login(request.short_url, request.phone_number, request.password)
        logger.info(f"URL étendue récupérée : {expanded_url}")
        return {"expanded_url": expanded_url}
    except Exception as e:
        logger.error(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail=str(e))
