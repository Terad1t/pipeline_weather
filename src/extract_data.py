import requests
import json
from pathlib import Path
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
api_key = os.getenv("API_KEY")
print("API_KEY:", api_key)

url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={api_key}'

def extract_data(url:str) -> list:
     
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error(f"Erro na requisição: {response.status_code} - {data}")

        return []
     
    if not data:
        logging.warning("Nenhum dado encontrado na resposta.")
        return []

    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Dados extraídos e salvos em {output_path}")

    return data

extract_data(url)