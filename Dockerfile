# Usar imagen oficial ligera de Python
FROM python:3.11-slim

# Evitar escritura de archivos .pyc y activar unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Copiar e instalar dependencias de la aplicación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY app/ app/

# Crear un usuario no-root por seguridad
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app/main.py"]
