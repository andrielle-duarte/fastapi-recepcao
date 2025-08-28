from pydantic import BaseModel, field_validator, model_validator, EmailStr
from datetime import datetime
from typing import Optional



# Entrada Visitante

class VisitanteCreate(BaseModel):
    nome: str
    documento: str
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    

    @field_validator('nome')
    def nome_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v

    @field_validator('documento')
    def documento_valido(cls, v):
        if not v or not v.strip():
            raise ValueError('Documento não pode ser vazio')
        return v

    @field_validator('motivo_visita')
    def motivo_valido(cls, v):
        if not v or not v.strip():
            raise ValueError('Motivo da visita não pode ser vazio')
        if len(v) > 255:
            raise ValueError('Motivo muito grande (máx. 255 caracteres)')
        return v

    @model_validator(mode="before")
    def validar_datas(cls, values):
        data_entrada = values.get('data_entrada')
        data_saida = values.get('data_saida')
        if data_entrada and data_saida:
            de = data_entrada.replace(tzinfo=None) if data_entrada.tzinfo else data_entrada
            ds = data_saida.replace(tzinfo=None) if data_saida.tzinfo else data_saida
            if ds < de:
                raise ValueError('Data de saída não pode ser anterior à data de entrada')
        return values


# Saída Visitante

class VisitanteOut(BaseModel):
    id: int
    nome: str
    documento: Optional[str] = None
    motivo_visita: Optional[str] = None
    data_entrada: Optional[datetime] = None
    

    @field_validator('documento', mode='before')
    def mascarar_documento(cls, v):
        if v and len(v) >= 5:
            return v[:3] + "****" + v[-2:]
        return v

    class Config:
        from_attributes = True


# Entrada Visita

class VisitaCreate(BaseModel):
    visitante_id: int
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None


# Saída Visita

class VisitaOut(BaseModel):
    id: int
    visitante_id: int
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None
    visitante: Optional[VisitanteOut] = None

    class Config:
        from_attributes = True



class RecepcionistaBase(BaseModel):
    nome: str
    email: EmailStr
    admin: bool = False

class RecepcionistaCreate(RecepcionistaBase):
    senha: str

class RecepcionistaOut(RecepcionistaBase):
    id: int

class Login(BaseModel):
    email: str
    senha: str

    class Config: 
        from_attributes = True

class MotivoRequest(BaseModel):
    motivo_visita: str