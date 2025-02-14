import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Accéder à Facebook et se connecter
        logger.info(f"Accès à Facebook")
        driver.get("https://www.facebook.com/")

        # Attendre que la page de connexion s'affiche
        time.sleep(3)

        # Remplir les informations de connexion
        phone_input = driver.find_element(By.ID, "email")  # ID du champ email (modifié si nécessaire)
        password_input = driver.find_element(By.ID, "pass")  # ID du champ mot de passe (modifié si nécessaire)

        phone_input.send_keys(phone_number)
        password_input.send_keys(password)

        # Soumettre le formulaire
        password_input.send_keys(Keys.RETURN)

        # Attendre la redirection après la connexion
        time.sleep(5)

        # Maintenant, nous allons charger l'URL raccourcie
        logger.info(f"Accès à l'URL raccourcie : {short_url}")
        driver.get(short_url)

        # Attendez un peu pour que la page se charge après avoir accédé à l'URL
        time.sleep(3)

        # Récupérer l'URL finale
        expanded_url = driver.current_url

        logger.info(f"URL finale : {expanded_url}")
    except Exception as e:
        logger.error(f"Erreur lors du traitement : {e}")
        raise
    finally:
        driver.quit()

    return expanded_url

@app.post("/unshorten/")
async def unshorten_url(request: UnshortenRequest):
    try:
        logger.info(f"Requête reçue avec URL : {request.short_url}")
        expanded_url = unshorten_url_with_login(request.short_url, request.phone_number, request.password)
        return {"expanded_url": expanded_url}
    except Exception as e:
        logger.error(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail=str(e))
