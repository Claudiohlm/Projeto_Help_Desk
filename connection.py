# arquivo para configuração da conexão com o banco de dados

from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import OperationalError

# carrega o .env
load_dotenv()

# pega a URL do banco
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# valida se encontrou a variável
if not SQLALCHEMY_DATABASE_URI:
    raise ValueError("A variável DATABASE_URL não foi encontrada no arquivo .env")

# cria engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_pre_ping=True
)

# base ORM
Base = declarative_base()

# teste de conexão
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Banco de dados conectado com sucesso!")

except OperationalError as e:
    print("❌ Falha na conexão com o banco!")
    print(e)