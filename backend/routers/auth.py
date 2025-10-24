from core.security import bcrypt_context
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import schemas
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt, JWTError
from models import Recepcionista
import requests
from dotenv import load_dotenv

load_dotenv()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL")
CLIENT_ID = os.getenv("CLIENT_ID")

router = APIRouter(prefix="/auth", tags=["auth"])

JWKS_URL = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

try:
    response = requests.get(JWKS_URL, timeout=25)
    response.raise_for_status()
    jwks = response.json()
except requests.RequestException:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Não está conectado ao Keycloak."
    )
except ValueError:
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Resposta inválida do Keycloak."
    )

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    try:
        header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
        if not key:
            raise HTTPException(status_code=401, detail="Chave pública do token não encontrada.")

        payload = jwt.decode(token, key, algorithms=["RS256"], audience="account")
        recepcionista = session.query(Recepcionista).filter(Recepcionista.email == payload.get("email")).first()
        if not recepcionista:
            recepcionista = Recepcionista(
                nome=payload.get("name"),
                email=payload.get("email"),
                senha="autenticado-keycloak",
                admin="admin" in payload.get("realm_access", {}).get("roles", [])
            )
            session.add(recepcionista)
            session.commit()
            session.refresh(recepcionista)
        return recepcionista

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/criar_conta", response_model=schemas.RecepcionistaOut)
async def criar_conta(
    dados: schemas.RecepcionistaCreate,
    db: Session = Depends(get_db),
    recepcionista: Recepcionista = Depends(get_current_user)  
):
    if not recepcionista.admin:
        raise HTTPException(status_code=401, detail="Você não pode criar um novo recepcionista sem ser administrador.")
    novo_recepcionista = Recepcionista(
        nome=dados.nome,
        email=dados.email,
        senha=bcrypt_context.hash(dados.senha),
        admin=dados.admin
    )
    db.add(novo_recepcionista)
    db.commit()
    db.refresh(novo_recepcionista)
    return novo_recepcionista
