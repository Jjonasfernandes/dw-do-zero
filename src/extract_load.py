import os
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

commodities = ['CL=F', 'GC=F', 'SI=F']

DB_HOST = os.gentenv('DB_HOST_PROD')
DB_PORT = os.gentenv('DB_PORT_PROD')
DB_NAME = os.gentenv('DB_NAME_PROD')
DB_USER = os.gentenv('DB_USER_PROD')
DB_PASS = os.gentenv('DB_PASS_PROD')
DB_SCHEMA = os.gentenv('DB_SCHEMA_PROD')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engone = create_engine(DATABASE_URL)
def buscar_dados_commodities(simbolo, periodo='5y', intervalo='1d'):
  ticker = yf.Ticker(simbolo)
  dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
  dados['simbolo'] = simbolo
  return dados


def buscar_todos_dados_commodities(commodities):
  todos_dados = []
  for simbolo in commodities:
    dados = buscar_dados_commodities(simbolo)
    todos_dados.append(dados)
  return pd.concat(todos_dados)

def salvar_no_postgres(df, schema='public'):
  df.to_sql('commodities', engine, if_exists='replace', index=True, index_label='Date', schema=schema)


if __name__ == '__main__':
  dados_concatenados = buscar_todos_dados_commodities(commodities)
  print(dados_concatenados)