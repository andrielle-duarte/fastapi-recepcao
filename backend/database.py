import os
import re
from urllib.parse import quote_plus
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_USER = os.getenv("DB_USER", "").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()
DB_HOST = os.getenv("DB_HOST", "").strip()
DB_PORT = os.getenv("DB_PORT", "").strip()
DB_NAME = os.getenv("DB_NAME", "").strip()

#Pra nao aatrapalhar com senhas com caracteres especiais 
escaped_password = quote_plus(DB_PASSWORD)

# Verificação  obrigatoria
required_vars = [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]
if not all(required_vars):
    raise ValueError("Uma ou mais variáveis de ambiente do banco de dados estão faltando.")

# Porta padrão caso não esteja definida corretamente
DB_PORT = int(DB_PORT) if DB_PORT and DB_PORT.lower() != 'none' else 3306

#Função pra mascarar a senha na url de conexão com banco de dados
def _mask_password(url: str) -> str:
    """Mascarar a senha em uma URL de conexão para logs."""
    return re.sub(r"(://[^:]+:)([^@]+)(@)", r"\1***\3", url)
# String de conexão
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("Conectando ao banco:", _mask_password(SQLALCHEMY_DATABASE_URL))




# Engine e sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para os modelos ORM
Base = declarative_base()

# Dependência para uso com FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
