FROM python:3.11-slim

# Impedir de gravar .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# força os logs a aparecerem no terminal
ENV PYTHONBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Liga no servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]