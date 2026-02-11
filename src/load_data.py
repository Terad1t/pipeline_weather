from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path    
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", "5432")

def get_engine():
    logging.info(f"+ Conectando em {host}:{port}/{database} com usuário {user}")
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str, df:pd.DataFrame):
    df.to_sql(
        name = table_name,
        con=engine,
        if_exists='append',
        index=False
    )
    logging.info(f"Dados carregados na tabela {table_name} com sucesso!")

    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)
    logging.info(f"Verificação: {len(df_check)} registros encontrados na tabela {table_name}.")


