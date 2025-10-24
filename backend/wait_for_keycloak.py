import time
import requests

KEYCLOAK_URL = "http://keycloak:8080/realms/recepcao"
MAX_RETRIES = 120  # 120 tentativas (~2 minutos)
SLEEP_SECS = 5

for i in range(MAX_RETRIES):
    try:
        response = requests.get(KEYCLOAK_URL)
        if response.status_code == 200:
            print("Keycloak pronto! Iniciando backend...")
            break
    except Exception:
        pass
    print(f"Aguardando Keycloak ({i+1}/{MAX_RETRIES})...")
    time.sleep(SLEEP_SECS)
else:
    print("Keycloak não respondeu a tempo.")
    exit(1)

import os
os.system("uvicorn main:app --host 0.0.0.0 --port 8000")
