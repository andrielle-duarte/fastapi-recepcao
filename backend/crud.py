from fastapi import  HTTPException
from sqlalchemy.orm import Session
from backend import database, models, schemas, crud
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from .database import get_db


# Retorna todos os visitantes, com suporte a paginação (skip e limit)
def get_visitantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitante).offset(skip).limit(limit).all()

# Busca um visitante específico pelo ID
def get_visitante(db: Session, visitante_id: int):
    return db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()



def listar_visitas_por_visitante(db, visitante_id):
    return db.query(models.Visita).filter(models.Visita.visitante_id == visitante_id).all()




def create_visitante(db: Session, visitante: schemas.VisitanteCreate):
    data_entrada = visitante.data_entrada or None
    
    db_visitante = models.Visitante(
        nome=visitante.nome,
        documento=visitante.documento,
        motivo_visita=visitante.motivo_visita,
        data_entrada=data_entrada,  
        data_saida=visitante.data_saida,
    )
    db.add(db_visitante)
    db.commit()
    db.refresh(db_visitante)
    return db_visitante


from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from backend import models, schemas

def iniciar_visita(db: Session, visita: schemas.VisitaCreate):
    
    visita_ativa = db.query(models.Visita).filter(
        and_(
            models.Visita.visitante_id == visita.visitante_id,
            models.Visita.data_saida == None  
        )
    ).first()

    if visita_ativa:
        raise HTTPException(status_code=400, detail=f"{visita_ativa.visitante.nome} já possui visita ativa 👍")


    
    nova_visita = models.Visita(
        visitante_id=visita.visitante_id,
        motivo_visita=visita.motivo_visita,
    )
    db.add(nova_visita)
    db.commit()
    db.refresh(nova_visita)
    return nova_visita



def iniciar_visita_existente(db: Session, visitante_id: int, visitante_dados: schemas.VisitanteCreate):
    db_visitante = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()

    if not db_visitante:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")

    if db_visitante.data_entrada and not db_visitante.data_saida:
        raise HTTPException(status_code=400, detail="Visita já está ativa")

    # Atualiza data_entrada e reseta data_saida
    db_visitante.data_entrada = visitante_dados.data_entrada or models.now_brasilia()
    db_visitante.data_saida = None

    db.commit()
    db.refresh(db_visitante)

    return db_visitante


# Atualiza os dados de um visitante existente
def edit_visitante(db: Session, request: schemas.VisitanteCreate, old_db_visitante: models.Visitante):
    old_db_visitante.nome = request.nome
    old_db_visitante.documento = request.documento
    old_db_visitante.motivo_visita = request.motivo_visita
    old_db_visitante.data_entrada = request.data_entrada
    old_db_visitante.data_saida = request.data_saida
    db.commit()                    
    db.refresh(old_db_visitante)  
    return old_db_visitante

# Remove um visitante do banco, se existir
def delete_visitante(db: Session, visitante_id: int):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        return None               
    db.delete(visitante_db)       
    db.commit()                   
    return visitante_db
