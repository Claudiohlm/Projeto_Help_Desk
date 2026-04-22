# arquivo para configuraçao da conexao com o banco de dados
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError


load_dotenv()


SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_pre_ping=True
)

Base = declarative_base()

try:
    with engine.connect() as connection:
        print("Banco de dados Conectado!")
except OperationalError as e:
    print("Falha na conexão!")