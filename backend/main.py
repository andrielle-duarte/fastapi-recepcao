from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db


# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Configuração CORS para permitir chamadas do frontend em localhost:5174
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Ajuste para sua porta do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raiz para checar status da API
@app.get("/")
def root():
    return {"status": "Sistema de recepção ativo"}

# Criar visitante 
@app.post("/visitantes/", response_model=schemas.VisitanteOut)
def create_visitante(visitante: schemas.VisitanteCreate, db: Session = Depends(get_db)):
    return crud.create_visitante(db=db, visitante=visitante)

# Listar visitantes com paginação (skip)
@app.get("/visitantes/", response_model=list[schemas.VisitanteOut])
def get_visitantes(skip: int = 0, db: Session = Depends(get_db)):
    visitantes = crud.get_visitantes(db, skip=skip)
    return visitantes
    
# Buscar visitante por id
@app.get("/visitantes/{visitante_id}", response_model=schemas.VisitanteOut)
def get_visitante(visitante_id: int, db: Session = Depends(get_db)):
    visitante = crud.get_visitante(db, visitante_id=visitante_id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")
    return visitante

# Atualizar visitante
@app.put("/visitantes/{visitante_id}", response_model=schemas.VisitanteOut)
def edit_visitante(visitante_id: int, request: schemas.VisitanteCreate, db: Session = Depends(get_db)):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if visitante_db is None:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")

    # Atualiza campos com os dados da requisição
    visitante_db.nome = request.nome
    visitante_db.documento = request.documento
    visitante_db.motivo_visita = request.motivo_visita
    visitante_db.data_entrada = request.data_entrada
    visitante_db.data_saida = request.data_saida

    db.commit()
    db.refresh(visitante_db)
    return visitante_db

# Deletar visitante pelo id
@app.delete("/visitantes/{visitante_id}", status_code=204)
def delete_visitante(visitante_id: int, db: Session = Depends(get_db)):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")
    db.delete(visitante_db)
    db.commit()