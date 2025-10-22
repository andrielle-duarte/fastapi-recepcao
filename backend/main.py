from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from backend.routers.visitas import router as visitas_router
from backend.routers.visitantes import router as visitantes_router
from backend.routers.auth import get_current_user, router as auth_router
from . import  models
from .database import engine
import logging

app = FastAPI(
    title="Sistema de Recepção do Ifrj",
    description="API para gerenciar visitantes e visitas no Ifrj",
    version="1.0.0",
)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "bearer"}

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


app.include_router(auth_router)
app.include_router(visitas_router)
app.include_router(visitantes_router)


# Cria as tabelas no banco de dados (se não existirem)
models.Base.metadata.create_all(bind=engine)

#Botar em variável de ambiente depois
origins = [
    "http://localhost:5173"
]

# Configuração CORS para permitir chamadas do frontend em localhost:5174 ou 73 
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint raiz para checar status da API

@app.get("/public")
def public():
    return {"msg": "Rota pública, sem autenticação"}

@app.get("/private")
def private(user: dict = Depends(get_current_user)):
    return {"msg": "Rota protegida", "user": user}
