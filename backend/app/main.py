from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api.routes import router

# Cria as tabelas no banco de dados
# O metadata contém uma lista de todas as classes que herdaram de Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GeoAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # URL do seu React
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, DELETE, etc.
    allow_headers=["*"], # Permite todos os headers
)

@app.get("/")
def root():
    return {"message": "GeoAPI online"}

app.include_router(router)