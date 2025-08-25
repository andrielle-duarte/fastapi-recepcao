from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Config do bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")