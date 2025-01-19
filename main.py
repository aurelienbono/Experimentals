from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def login_and_unshorten(short_url, email, password):
    # Configuration du WebDriver
    service = Service('/usr/bin/chromedriver')  # Chemin vers Chromedriver (installé via Docker)
    options = Options()
    options.add_argument("--headless")  # Mode headless pour l'exécution sans interface graphique
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Lancer le navigateur
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Étape 1 : Accéder à Facebook Login
        driver.get("https://www.facebook.com/login")
        time.sleep(3)

        # Entrer l'email
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(email)

        # Entrer le mot de passe
        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Attendre le chargement après connexion

        # Étape 2 : Aller vers l'URL raccourcie
        driver.get(short_url)
        time.sleep(5)  # Attendre la redirection

        # Capturer l'URL finale
        original_url = driver.current_url
    finally:
        driver.quit()

    return original_url

email = "237696330904"
password = "Nath@love01"
short_url = "https://fb.watch/w_icwPLBJM/"  

original_url = login_and_unshorten(short_url, email, password)
print("URL d'origine :", original_url)
