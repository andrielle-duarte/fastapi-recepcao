from typing import List
from fastapi import APIRouter, Body, Depends,  HTTPException
from sqlalchemy.orm import Session
from backend import crud, models, schemas
from backend.database import get_db
from backend.models import Visita
from datetime import datetime
from ..database import get_db
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/visitas", tags=["Visitas"])
def now_brasilia():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))



# Iniciar uma nova visita (registra data_entrada, motivo, etc)
@router.post("/", response_model=schemas.VisitaOut)
def iniciar_visita(visita: schemas.VisitaCreate, db: Session = Depends(get_db)):
    """
    Rota para iniciar visita.
    """
    return crud.iniciar_visita(db=db, visita=visita)

@router.get("/ativas", response_model=List[schemas.VisitaOut])
def listar_visitas_ativas(db: Session = Depends(get_db)):
    """
    Rota para listar visitas ativas .
    """
    visitas_ativas = db.query(models.Visita).filter(
        models.Visita.data_saida == None,
        models.Visita.visitante_id != None
        ).all()
    for visita in visitas_ativas:
        visita.visitante  
    return visitas_ativas

# Histórico de todas as visitas, futuramente aplicar filtro por data 
@router.get("/historico/")
def get_historico(db: Session = Depends(get_db)):
    """
    Roata para listar todas as visitas e filtra-las por datas .
    """
    visitas = db.query(models.Visita).all()
    resultado = []

    for v in visitas:
        visitante = db.query(models.Visitante).filter(models.Visitante.id == v.visitante_id).first()
        resultado.append({
            "id": v.id,
            "motivo_visita": v.motivo_visita,
            "data_entrada": v.data_entrada,
            "data_saida": v.data_saida,
            "nome": visitante.nome if visitante else "",
            "documento": visitante.documento if visitante else ""
        })

    return resultado

# Obter histórico de visitas de um visitante
@router.get("/historico/{visitante_id}", response_model=List[schemas.VisitaOut])
def historico_visitante(visitante_id: int, db: Session = Depends(get_db)):
    """
    Rota para retornar o histórico de um visitante por id.
    """
    return db.query(models.Visita).filter(models.Visita.visitante_id == visitante_id).all()


# Alterar motivo da visita em andamento de um visitante
@router.put("/visitantes/{visitante_id}/alterar-motivo", response_model=schemas.VisitanteOut)
def alterar_motivo(visitante_id: int, motivo: schemas.MotivoRequest, db: Session = Depends(get_db)):
    
    visitante = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante:
        raise HTTPException(status_code=200, detail="Visitante não encontrado")
    
    visitante.motivo_visita = motivo.motivo_visita 
    db.commit()
    db.refresh(visitante)
    return visitante

@router.put("/{visita_id}/encerrar")
def encerrar_visita(visita_id: int, db: Session = Depends(get_db)):
    """
    Rota para encerrar visita.
    """
    visita = db.query(Visita).filter(Visita.id == visita_id).first()
    if not visita:
        raise HTTPException(status_code=200, detail="Visita não encontrada")
    if visita.data_saida:
        raise HTTPException(status_code=200, detail="Visita já encerrada")

    visita.data_saida = now_brasilia() 
    db.commit()
    db.refresh(visita)
    return visita