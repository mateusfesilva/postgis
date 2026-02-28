# WebGIS Backend - FastAPI & PostGIS

Este projeto é uma API REST para gerenciamento de dados vetoriais, desenvolvida para demonstrar a integração entre **Python (FastAPI)** e bancos de dados espaciais (**PostGIS**).

## Tecnologias Utilizadas
* **FastAPI**
* **PostGIS**
* **SQLAlchemy & GeoAlchemy2**
* **Docker & Docker Compose**

## Como rodar o projeto
1. Clone o repositório: `git clone ...`
2. Crie um arquivo `.env` baseado no `.env.example`.
3. Suba o ambiente com Docker:
   ```bash
   docker compose up -d --build