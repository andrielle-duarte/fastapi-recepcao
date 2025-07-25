from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from backend import crud, models, schemas
from backend.database import get_db
from backend.models import Visita
from datetime import datetime
router = APIRouter(prefix="/visitas", tags=["Visitas"])



# Iniciar uma nova visita (registra data_entrada, motivo, etc)
@router.post("/", response_model=schemas.VisitaOut)
def iniciar_visita(visita: schemas.VisitaCreate, db: Session = Depends(get_db)):
    return crud.iniciar_visita(db=db, visita=visita)

# Alterar motivo da visita em andamento de um visitante
@router.put("/visitantes/{visitante_id}/alterar-motivo", response_model=schemas.VisitanteOut)
def alterar_motivo(visitante_id: int, motivo: dict, db: Session = Depends(get_db)):
    visitante = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante:
        raise HTTPException(status_code=200, detail="Visitante não encontrado")
    
    visitante.motivo_visita = motivo.get("motivo_visita")
    db.commit()
    db.refresh(visitante)
    return visitante

# Obter histórico de visitas de um visitante
@router.get("/historico/{visitante_id}", response_model=List[schemas.VisitaOut])
def historico_visitas(visitante_id: int, db: Session = Depends(get_db)):
    return db.query(models.Visita).filter(models.Visita.visitante_id == visitante_id).all()

@router.get("/historico/teste")
def test_route():
    return {"message": "Rota funcionando"}

@router.put("/{id}/encerrar")
def encerrar_visita(id: int, db: Session = Depends(get_db)):
    visita = db.query(Visita).filter(Visita.id == id).first()
    if not visita:
        raise HTTPException(status_code=404, detail="Visita não encontrada")
    
    visita.data_saida = datetime.now()
    print(f"Encerrando visita {visita.id} com data de saída {visita.data_saida}")  # Debug
    
    db.commit()
    db.refresh(visita)
    return visita
