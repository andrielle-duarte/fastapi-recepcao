from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter()

#nao ta puxando daqui, quando colocar visitas tem que organizar


@router.get("/visitantes/buscar", response_model=list[schemas.VisitanteOut])
def buscar_visitantes(termo: str = Query(...), db: Session = Depends(get_db)):
    visitantes = db.query(models.Visitante).filter(
        (models.Visitante.nome.ilike(f"%{termo}%")) |
        (models.Visitante.documento.ilike(f"%{termo}%"))
    ).all()
    return visitantes

@router.post("/visitas/", response_model=schemas.VisitanteOut)
def criar_visitante(visitante: schemas.VisitanteCreate, db: Session = Depends(get_db)):
    db_visitante = models.Visitante(
        nome=visitante.nome,
        documento=visitante.documento,
        motivo_visita=visitante.motivo_visita,
        data_entrada=visitante.data_entrada,
        data_saida=visitante.data_saida
    )
    db.add(db_visitante)
    db.commit()
    db.refresh(db_visitante)
    return db_visitante

@router.put("/visitantes/{visitanteId}/alterar-motivo")
def alterar_motivo(id: int, motivo: dict, db: Session = Depends(get_db)):
    visitante = db.query(models.Visitante).filter(models.Visitante.id == id).first()
    if not visitante:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")
    
    visitante.motivo_visita = motivo["motivo_visita"]
    db.commit()
    db.refresh(visitante)
    return visitante