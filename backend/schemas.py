from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

# Schema para entrada (criação/edição de visitante)
class VisitanteCreate(BaseModel):
    nome: str
    documento: str
    motivo_visita: str
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None

    # Valida que o nome não pode ser vazio ou só espaços
    @field_validator('nome')
    def nome_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome não pode ser vazio')
        return v

    # Valida que documento não é vazio e contém só números
    @field_validator('documento')
    def documento_nao_vazio_e_numerico(cls, v):
        if not v or not v.strip():
            raise ValueError('Documento não pode ser vazio')
        if not v.isdigit():
            raise ValueError('Documento deve conter apenas números')
        return v

    # Valida que data_saida, se fornecida, não é anterior a data_entrada
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

# Schema para saída de dados do visitante (response)
class VisitanteOut(BaseModel):
    id: int
    nome: str
    documento: str
    motivo_visita: Optional[str] = None
    data_entrada: Optional[datetime] = None
    data_saida: Optional[datetime] = None

    # Validação extra para garantir documento só números (pode ajudar em outputs que passam por transformação)
    @field_validator('documento')
    def documento_so_numeros(cls, v):
        if not v.isdigit():
            raise ValueError('Documento deve conter apenas números')
        return v

    class Config:
        # Permite que o Pydantic aceite dados vindos de objetos ORM (models SQLAlchemy)
        from_attributes = True

class VisitaCreate(BaseModel):
    visitante_id: int
    motivo_visita: str
    data_entrada: datetime
    data_saida: Optional[datetime] = None
    
class VisitaOut(BaseModel):
    id: int
    visitante_id: int
    motivo_visita: str
    data_entrada: datetime
    data_saida: Optional[datetime] = None

    class Config:
        from_atributes = True