from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")



# Config do bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# OAuth2 schema
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")