from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from sqlalchemy import or_
from backend import database
from backend.routers.visitas import router as visitas_router
from backend.routers.visitantes import router as visitantes_router
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from typing import List

app = FastAPI()


app.include_router(visitas_router)
app.include_router(visitantes_router)


# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)



# Configuração CORS para permitir chamadas do frontend em localhost:5174 ou 73 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raiz para checar status da API
@app.get("/")
def root():
    return {"status": "Sistema de recepção ativo"}

