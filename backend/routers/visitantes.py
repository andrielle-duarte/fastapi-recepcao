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


# Atualizar visitante - usado para nova visita por enquanto
@router.put("/{visitante_id}/iniciar", response_model=schemas.VisitanteOut)
def edit_visitante(visitante_id: int, request: schemas.VisitanteCreate, db: Session = Depends(get_db)):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if visitante_db is None:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")

    visitante_db.nome = request.nome
    visitante_db.documento = request.documento
    visitante_db.motivo_visita = request.motivo_visita
    visitante_db.data_entrada = request.data_entrada
    visitante_db.data_saida = request.data_saida

    db.commit()
    db.refresh(visitante_db)
    return visitante_db


# Encerrar visita
@router.put("/{id}/encerrar", response_model=schemas.VisitanteOut)
def encerrar_visita(id: int, db: Session = Depends(get_db)):
    visitante = crud.get_visitante(db, id)
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")
    if visitante.data_saida:
        raise HTTPException(status_code=400, detail="Visita já encerrada")

    visitante.data_saida = datetime.now(timezone.utc)
    db.commit()
    db.refresh(visitante)
    return visitante

#nao encerra com a data de saida 
#navbar unico 
#contagem de visita ao encerrar ???


# Deletar visitante
@router.delete("/{visitante_id}", status_code=204)
def delete_visitante(visitante_id: int, db: Session = Depends(get_db)):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")
    db.delete(visitante_db)
    db.commit()
