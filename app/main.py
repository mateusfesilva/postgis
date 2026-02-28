from fastapi import FastAPI, HTTPException, Depends
from .database import engine, Base
from .routes import router

# Cria as tabelas no banco de dados
# O metadata contém uma lista de todas as classes que herdaram de Base
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GeoAPI")

@app.get("/")
def root():
    return {"message": "GeoAPI online" }

app.include_router(router)