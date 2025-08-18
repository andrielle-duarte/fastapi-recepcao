from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from backend import models, schemas


# Visitante

def get_visitantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitante).offset(skip).limit(limit).all()

def get_visitante(db: Session, visitante_id: int):
    return db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()

def create_visitante(db: Session, visitante: schemas.VisitanteCreate):
    visitante_existente = db.query(models.Visitante).filter(
        or_(
            models.Visitante.documento == visitante.documento,
            models.Visitante.nome == visitante.nome
        )
    ).first()

    if visitante_existente:
        if visitante_existente.documento == visitante.documento:
            raise HTTPException(status_code=400, detail="Visitante com este documento já existe.")
        if visitante_existente.nome == visitante.nome:
            raise HTTPException(status_code=400, detail="Visitante com este nome já existe.")

    db_visitante = models.Visitante(
        nome=visitante.nome.strip(),
        documento=visitante.documento.strip(),
        motivo_visita=visitante.motivo_visita,
        data_entrada=visitante.data_entrada or None,
    )
    db.add(db_visitante)
    db.commit()
    db.refresh(db_visitante)
    return db_visitante


def edit_visitante(db: Session, request: schemas.VisitanteCreate, old_db_visitante: models.Visitante):
    old_db_visitante.nome = request.nome
    old_db_visitante.documento = request.documento
    old_db_visitante.motivo_visita = request.motivo_visita
    old_db_visitante.data_entrada = request.data_entrada
    old_db_visitante.data_saida = request.data_saida
    db.commit()                    
    db.refresh(old_db_visitante)  
    return old_db_visitante

def delete_visitante(db: Session, visitante_id: int):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        return None               
    db.delete(visitante_db)       
    db.commit()                   
    return visitante_db


# Visita

def get_visitas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visita).offset(skip).limit(limit).all()

def listar_visitas_por_visitante(db: Session, visitante_id: int):
    return db.query(models.Visita).filter(models.Visita.visitante_id == visitante_id).all()

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


# Visitas ativa (otimizada), nao busca na lista toda 

def listar_visitas_ativas(db: Session, visitante_id: int = None):
    query = db.query(models.Visita).filter(models.Visita.data_saida == None)
    if visitante_id is not None:
        query = query.filter(models.Visita.visitante_id == visitante_id)
    return query.all()
