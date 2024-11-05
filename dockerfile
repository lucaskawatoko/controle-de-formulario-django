FROM python:3.11.3-alpine3.18
LABEL maintainer="lucaskawatoko@gmail.com"

# Variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências necessárias
RUN apk add --no-cache bash curl inotify-tools

# Instalar dependências necessárias
RUN apk add --no-cache bash curl


# Copiar a pasta django_app e scripts para o container
COPY django_app /django_app
COPY scripts /scripts

# Definir diretório de trabalho
WORKDIR /django_app

# Expor a porta 8000
EXPOSE 8000

# Instalar dependências do Python, criar e configurar diretórios
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /django_app/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /venv && \
    chown -R duser:duser /data/web/static && \
    chown -R duser:duser /data/web/media && \
    chmod -R 755 /data/web/static && \
    chmod -R 755 /data/web/media && \
    chmod -R +x /scripts

# Definir PATH para incluir scripts e venv
ENV PATH="/scripts:/venv/bin:$PATH"

# Definir o usuário para rodar o container
USER duser

# Comando para iniciar a aplicação
CMD ["commands.sh"]
