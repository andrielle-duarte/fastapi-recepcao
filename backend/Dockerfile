FROM python:3.13-slim

WORKDIR /app

# aqui o requirements.txt vem da pasta backend/ do host,
# mas dentro da imagem fica em /app/requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO o código do backend para /app/backend
COPY . /app/backend

ENV PYTHONPATH=/app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
