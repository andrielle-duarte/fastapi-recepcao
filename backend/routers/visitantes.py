from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend import crud, models, schemas
from backend.database import get_db

router = APIRouter(prefix="/visitantes", tags=["Visitantes"])


# Criar visitante
@router.post("/", response_model=schemas.VisitanteOut)
def create_visitante(visitante: schemas.VisitanteCreate, db: Session = Depends(get_db)):
    return crud.create_visitante(db=db, visitante=visitante)


# Listar visitantes com paginação
@router.get("/", response_model=List[schemas.VisitanteOut])
def get_visitantes(skip: int = 0, db: Session = Depends(get_db)):
    visitantes = crud.get_visitantes(db, skip=skip)
    return visitantes


# Buscar visitante por nome ou documento
@router.get("/buscar", response_model=List[schemas.VisitanteOut])
def buscar_visitantes(termo: str = "", db: Session = Depends(get_db)):
    visitantes = db.query(models.Visitante).filter(
        (models.Visitante.nome.ilike(f"%{termo}%")) |
        (models.Visitante.documento.ilike(f"%{termo}%"))
    ).all()
    return visitantes





#nao encerra com a data de saida 
#navbar unico 
#contagem de visita ao encerrar ???


# Deletar visitante
@router.delete("/{visitante_id}", status_code=204)
def delete_visitante(visitante_id: int, db: Session = Depends(get_db)):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        raise HTTPException(status_code=200, detail="Visitante não encontrado")
    db.delete(visitante_db)
    db.commit()
 