FROM python:3.12-slim

# Evita criação de arquivos .pyc e força logs em tempo real no terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Garante que a pasta do banco exista e o script tenha permissão de execução
RUN mkdir -p /app/data && chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]