from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class VisitanteCreate(BaseModel):
    nome: str
    documento: str
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None

    @field_validator('nome')
    def nome_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v

    @field_validator('data_saida')
    def data_saida_maior_entrada(cls, v, info):
        data_entrada = info.data.get('data_entrada')
        if v and data_entrada:
            if v.tzinfo:
                v = v.replace(tzinfo=None)
            if data_entrada.tzinfo:
                data_entrada = data_entrada.replace(tzinfo=None)
            if v < data_entrada:
                raise ValueError('Data de saída não pode ser anterior à data de entrada')
        return v
    



class VisitanteOut(BaseModel):
    id: int
    nome: str
    documento: Optional[str] = None
    motivo_visita: Optional[str] = None
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None

    @field_validator('documento', mode='before')
    def mascarar_documento(cls, v):
        if v and len(v) >= 5:
            return v[:3] + "****" + v[-2:]
        return v


class VisitaCreate(BaseModel):
    visitante_id: int
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None


class VisitaOut(BaseModel):
    id: int
    visitante_id: int
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None
    visitante: Optional[VisitanteOut] = None

    class Config:
        from_attributes = True
