import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class UnshortenRequest(BaseModel):
    short_url: str

# Hardcoded cookies
cookies = [
    {"name": "c_user", "value": "100010150669481", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False, "sameSite": "no_restriction"},
    {"name": "datr", "value": "8fg8Zuw5qSqDAmong7Ty3DIc", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": True, "sameSite": "no_restriction"},
    {"name": "fr", "value": "136g7WrJBfJfcHQLV.AWXZs3drIym4K7wCAvxoD1rDjQ7zNIVz2QrgqQ.Bnr6Yz..AAA.0.0.Bnr6Yz.AWUIjjVHrOc", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": True, "sameSite": "no_restriction"},
    {"name": "presence", "value": "C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1739565149759%2C%22v%22%3A1%7D", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False, "sameSite": "unspecified"},
    {"name": "ps_l", "value": "1", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": True, "sameSite": "lax"},
    {"name": "ps_n", "value": "1", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": True, "sameSite": "no_restriction"},
    {"name": "sb", "value": "rld5ZrMcvNUwqZLmFWy7ydtY", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": True, "sameSite": "no_restriction"},
    {"name": "wd", "value": "1366x641", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": False, "sameSite": "lax"},
    {"name": "xs", "value": "16%3A0y0rbB1gFYNOaw%3A2%3A1719228538%3A-1%3A479%3A%3AAcVtrEy3DqrNimZqZYjscmFk_D8GZWUXyqrRR3qOb0w", "domain": ".facebook.com", "path": "/", "secure": True, "httpOnly": True, "sameSite": "no_restriction"}
]

def unshorten_url_with_cookies(short_url: str) -> str:
    logger.info(f"Début du traitement pour l'URL : {short_url}")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--user-data-dir=/tmp/chrome-profile")
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--no-sandbox") 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        logger.info(f"Accès à l'URL {short_url}")
        driver.get(short_url)
        driver.delete_all_cookies()

        logger.info("Ajout des cookies...")
        for cookie in cookies:
            driver.add_cookie({
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie['domain'],
                'path': cookie['path'],
                'expiry': cookie.get('expirationDate'),
                'secure': cookie['secure'],
                'httpOnly': cookie['httpOnly'],
                'sameSite': cookie.get('sameSite')
            })

        logger.info("Rechargement de la page après ajout des cookies...")
        driver.get(short_url)
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
        expanded_url = unshorten_url_with_cookies(request.short_url)
        return {"expanded_url": expanded_url}
    except Exception as e:
        logger.error(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail=str(e))
