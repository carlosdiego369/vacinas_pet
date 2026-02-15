# Vacinas Pets API - Docker
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências do sistema (se precisar de libs para psycopg2 no futuro)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Diretório do projeto Django (api + core)
ENV DJANGO_SETTINGS_MODULE=api.settings

# Coleta de static (opcional; descomente se usar arquivos estáticos no admin)
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Migrações rodam no entrypoint; servidor sobe com gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn api.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2"]
