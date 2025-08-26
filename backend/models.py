from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from zoneinfo import ZoneInfo

def now_brasilia():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

class Visitante(Base):
    __tablename__ = "visitantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    documento = Column(String(20), nullable=False, unique=True, index=True)
    motivo_visita = Column(String(255), nullable=False, index=True)
    data_entrada = Column(DateTime(timezone=True), default=now_brasilia)
    

    visitas = relationship(
        "Visita",
        back_populates="visitante",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True           
    )

class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    visitante_id = Column(Integer, ForeignKey("visitantes.id", ondelete="CASCADE"), nullable=False, index=True)
    motivo_visita = Column(String(255), nullable=False, index=True)
    data_entrada = Column(DateTime(timezone=True), default=now_brasilia)
    data_saida = Column(DateTime(timezone=True), nullable=True)

    visitante = relationship(
        "Visitante",
        back_populates="visitas",
        lazy="selectin",
        
    )


class Recepcionista(Base):
    __tablename__="recepcionista"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    senha = Column(String(100), nullable=False)
    admin = Column("admin", Boolean, default=False)
