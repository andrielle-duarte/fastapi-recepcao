from sqlalchemy.orm import Session
from backend import models, schemas


def get_visitante(db: Session, visitante_id: int):
    return db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()

def get_visitantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitante).offset(skip).limit(limit).all()


def create_visitante(db: Session, visitante: schemas.VisitanteCreate):
    db_visitante = models.Visitante(
        nome=visitante.nome,
        documento=visitante.documento,
        motivo_visita=visitante.motivo_visita,
        data_entrada=visitante.data_entrada,
        data_saida=visitante.data_saida,
    )
    db.add(db_visitante)
    db.commit()
    db.refresh(db_visitante)
    return db_visitante

def edit_visitante(db: Session, request: schemas.VisitanteCreate, old_db_visitante:models.Visitante):
    old_db_visitante.update({'nome':request.nome, 'documento':request.documento, 'motivo_visita':request.motivo_visita})
    db.commit()


def delete_visitante(db: Session, visitante_id: int):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        return None
    db.delete(visitante_db)
    db.commit()
    return visitante_db