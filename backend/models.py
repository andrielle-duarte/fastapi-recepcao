from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Modelo ORM Visitante que representa a tabela 'visitantes'
class Visitante(Base):
    __tablename__ = "visitantes"

    id = Column(Integer, primary_key=True)  # PK, índice para buscas rápidas
    nome = Column(String(100), nullable=False)                           # Nome do visitante (até 100 caracteres)
    documento = Column(String(20), nullable=False)       # Documento obrigatório (ex: RG, CPF)
    motivo_visita = Column(String(255), nullable=False)                  # Motivo da visita (até 255 caracteres)
    data_entrada = Column(DateTime(timezone=True), server_default=func.now())  # Data/hora da entrada, padrão horário atual UTC
    data_saida = Column(DateTime(timezone=True), nullable=True)        # Data/hora da saída, opcional


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    visitante_id = Column(Integer, ForeignKey("visitantes.id"))
    data_entrada = Column(DateTime, default=datetime.utcnow)
    data_saida = Column(DateTime, nullable=True)

    visitante = relationship("Visitante")