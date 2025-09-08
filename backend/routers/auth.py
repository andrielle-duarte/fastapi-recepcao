from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend import schemas
from backend.core.security import bcrypt_context, oauth2_schema, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from sqlalchemy.orm import Session
from backend.database import get_db
from jose import jwt, JWTError
from backend.models import Recepcionista
import requests

# Configurações do Keycloak
KEYCLOAK_URL = "http://localhost:8080/realms/recepcao"
CLIENT_ID = "recepcao-frontend"

router = APIRouter(prefix="/auth", tags=["auth"]) 


JWKS_URL = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


jwks = requests.get(JWKS_URL).json()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        header = jwt.get_unverified_header(token)
        key = None
        for k in jwks["keys"]:
            if k["kid"] == header["kid"]:
                key = k
        if not key:
            raise HTTPException(status_code=401, detail="Key not found")

        # Decodificar token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


##Autenticação local (sem Keycloak) - manter para compatibilidade

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_recepcionista = int(dic_info.get("id"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    # verificar se o token é válido
    # extrair o ID do usuário do token
    recepcionista = session.query(Recepcionista).filter(Recepcionista.id==id_recepcionista).first()
    if not recepcionista:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return recepcionista


def autenticar_recepcionista(email, senha, session):
    recepcionista = session.query(Recepcionista).filter(Recepcionista.email==email).first()
    if not recepcionista:
        return False
    elif not bcrypt_context.verify(senha, recepcionista.senha):
        return False
    return recepcionista

def criar_token(id_recepcionista, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"id": str(id_recepcionista), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


@router.get("/")
async def autenticar():
    """
    Rota para autenticar o sistema.
    """
    
    return {"mensagem":"Você acessou a rota padrão de autenticação", "autenticado": False}


@router.post("/criar_conta", response_model=schemas.RecepcionistaOut)
async def criar_conta(dados: schemas.RecepcionistaCreate, db: Session = Depends(get_db), recepcionista: Recepcionista = Depends(verificar_token)):
    if not recepcionista.admin:
        raise HTTPException(status_code=401, detail="Você não pode criar um novo recepcionista sem ser adminitrador.")
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



@router.post("/login")
async def login(login_schema: schemas.Login, session: Session = Depends(get_db)):
    recepcionista = autenticar_recepcionista(login_schema.email, login_schema.senha, session)
    if not recepcionista:
        raise HTTPException(status_code=400, detail="Recepcionista não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(recepcionista.id)
        refresh_token = criar_token(recepcionista.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }

@router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    recepcionista = autenticar_recepcionista(dados_formulario.username, dados_formulario.password, session)
    if not recepcionista:
        raise HTTPException(status_code=400, detail="Recepcionista não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(recepcionista.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }

    
@router.get("/refresh")
async def use_refresh_token(recepcionista: Recepcionista = Depends(verificar_token)):
    access_token = criar_token(recepcionista.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }
