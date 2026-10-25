# syntax=docker/dockerfile:1
# Python version comes from the root docker-compose.yml (build arg).
ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /FastApiBackend

# Dependencies first so this layer is cached until requirements.txt changes
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd --create-home appuser && chown -R appuser /FastApiBackend
USER appuser

EXPOSE 5000

# uvloop + httptools come from uvicorn[standard]. Push updates are not served here:
# events go to RabbitMQ and the Node socket server delivers them to browsers.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
