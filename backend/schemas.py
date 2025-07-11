from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional 

class VisitanteCreate(BaseModel):
    nome: str
    documento: str
    motivo_visita: Optional[str] = None
    data_entrada: datetime
    data_saida: Optional[datetime] = None

    @validator('nome')
    def nome_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v

    @validator('documento')
    def documento_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError('Documento não pode ser vazio')
        return v

    @validator('data_saida')
    def data_saida_maior_entrada(cls, v, values):
        data_entrada = values.get('data_entrada')
        if v and data_entrada and v < data_entrada:
            raise ValueError('Data de saída não pode ser anterior à data de entrada')
        return v


class VisitanteOut(BaseModel):
    id: int
    nome: str
    documento: str
    motivo_visita: Optional[str] = None
    data_entrada: datetime
    data_saida: Optional[datetime] = None


    class Config:
        orm_mode = True