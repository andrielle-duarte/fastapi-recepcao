from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database, models, schemas, crud
from datetime import datetime, timezone
from .database import get_db


# Retorna todos os visitantes, com suporte a paginação (skip e limit)
def get_visitantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Visitante).offset(skip).limit(limit).all()

# Busca um visitante específico pelo ID
def get_visitante(db: Session, visitante_id: int):
    return db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()



def listar_visitas_por_visitante(db, visitante_id):
    return db.query(models.Visita).filter(models.Visita.visitante_id == visitante_id).all()

def iniciar_visita_existente(visitante_id: int, visitante_dados: schemas.VisitanteCreate, db: Session = Depends(database.get_db)):
    db_visitante = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()

    if not db_visitante:
        raise HTTPException(status_code=404, detail="Visitante não encontrado")

    if db_visitante.data_entrada and not db_visitante.data_saida:
        raise HTTPException(status_code=400, detail="Visita já está ativa")

    db_visitante.data_entrada = visitante_dados.data_entrada
    db_visitante.data_saida = None
    db.commit()
    db.refresh(db_visitante)

    return db_visitante

# Cria e salva um novo visitante no banco de dados
def create_visitante(db: Session, visitante: schemas.VisitanteCreate):
    db_visitante = models.Visitante(
        nome=visitante.nome,
        documento=visitante.documento,
        motivo_visita=visitante.motivo_visita,
        data_entrada=visitante.data_entrada,
        data_saida=visitante.data_saida,
    )
    db.add(db_visitante)           # Adiciona à sessão do banco
    db.commit()                    # Confirma a transação
    db.refresh(db_visitante)      # Atualiza com os dados reais (ex: ID gerado)
    return db_visitante

# Cria e salva um novo visitante no banco de dados
def iniciar_visita(db: Session, visita: schemas.VisitaCreate):
    nova_visita = models.Visita(
        visitante_id=visita.visitante_id,
        motivo_visita=visita.motivo_visita,
        data_entrada=datetime.now(timezone.utc)
    )
    db.add(nova_visita)
    db.commit()
    db.refresh(nova_visita)
    return nova_visita

# Atualiza os dados de um visitante existente
def edit_visitante(db: Session, request: schemas.VisitanteCreate, old_db_visitante: models.Visitante):
    old_db_visitante.nome = request.nome
    old_db_visitante.documento = request.documento
    old_db_visitante.motivo_visita = request.motivo_visita
    old_db_visitante.data_entrada = request.data_entrada
    old_db_visitante.data_saida = request.data_saida
    db.commit()                    # Salva as alterações no banco
    db.refresh(old_db_visitante)  # Garante que os dados retornados estão atualizados
    return old_db_visitante

# Remove um visitante do banco, se existir
def delete_visitante(db: Session, visitante_id: int):
    visitante_db = db.query(models.Visitante).filter(models.Visitante.id == visitante_id).first()
    if not visitante_db:
        return None               # Se não encontrado, retorna None
    db.delete(visitante_db)       # Remove o visitante
    db.commit()                   # Confirma a exclusão
    return visitante_db
