from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from zoneinfo import ZoneInfo

def now_brasilia():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))


class Visitante(Base):
    __tablename__ = "visitantes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    documento = Column(String(20), nullable=False)
    motivo_visita = Column(String(255), nullable=False)
    data_entrada = Column(DateTime(timezone=True), default=now_brasilia)
    data_saida = Column(DateTime(timezone=True), nullable=True)

    visitas = relationship("Visita", back_populates="visitante")


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    visitante_id = Column(Integer, ForeignKey("visitantes.id"), nullable=False)
    motivo_visita = Column(String(255), nullable=False)
    data_entrada = Column(DateTime(timezone=True), default=now_brasilia)
    data_saida = Column(DateTime(timezone=True), nullable=True)
    visitante = relationship("Visitante", back_populates="visitas")
