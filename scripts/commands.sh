#!/bin/sh

set -e

# Esperar o banco de dados Postgres ficar disponível
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

# Coletar arquivos estáticos inicialmente
echo "🔄 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --ignore="*.scss" --ignore="sass/*"

# Aplicar migrações do banco de dados
echo "🔄 Aplicando migrações do banco de dados..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Iniciar o servidor Django em segundo plano
echo "🔄 Iniciando o servidor Django..."
python manage.py runserver 0.0.0.0:8000 &

# Iniciar o monitoramento de mudanças nos arquivos CSS
echo "🔄 Iniciando o monitoramento de mudanças nos arquivos CSS..."
while inotifywait -r -e modify,create,delete \
  /django_app/static/form/css \
  /django_app/static/registration/css \
  /django_app/static/cars/css; do
  echo "🔄 Mudanças detectadas nos arquivos CSS. Executando collectstatic..."
  python manage.py collectstatic --noinput --ignore="*.scss" --ignore="sass/*"
done

wait
