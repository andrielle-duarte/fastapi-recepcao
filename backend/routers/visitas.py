from typing import List
from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy.orm import Session
from backend import crud, models, schemas
from backend.database import get_db
from backend.models import Visita
from datetime import datetime, timezone
router = APIRouter(prefix="/visitas", tags=["Visitas"])



# Iniciar uma nova visita (registra data_entrada, motivo, etc)
@router.post("/", response_model=schemas.VisitaOut)
def iniciar_visita(visita: schemas.VisitaCreate, db: Session = Depends(get_db)):
    return crud.iniciar_visita(db=db, visita=visita)

@router.get("/ativas", response_model=List[schemas.VisitaOut])
def listar_visitas_ativas(db: Session = Depends(get_db)):
    visitas_ativas = db.query(models.Visita).filter(
        models.Visita.data_saida == None,
        models.Visita.visitante_id != None
        ).all()
    for visita in visitas_ativas:
        visita.visitante  
    return visitas_ativas

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


@router.put("/{visita_id}/encerrar")
def encerrar_visita(visita_id: int, db: Session = Depends(get_db)):
    visita = db.query(Visita).filter(Visita.id == visita_id).first()
    if not visita:
        raise HTTPException(status_code=200, detail="Visita não encontrada")
    if visita.data_saida:
        raise HTTPException(status_code=200, detail="Visita já encerrada")

    visita.data_saida = datetime.now(timezone.utc)
    db.commit()
    db.refresh(visita)
    return visita