from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from typing import List
from . import models, schemas
from .database import get_db

router = APIRouter()

# Organiza os paths dos endpoints (e agrupa no swagger)
@router.post("/pontos/", response_model=schemas.PontoResponse)
def create_ponto(ponto: schemas.CriarPonto, db: Session = Depends(get_db)):
    # lat/len para WKT
    wkt_element = f"POINT({ponto.longitude} {ponto.latitude})"

    db_ponto = models.GeometriaPonto(
        nome=ponto.nome,
        descricao=ponto.descricao,
        geom=wkt_element
    )
    db.add(db_ponto)
    db.commit()
    db.refresh(db_ponto)

    # Geom para lat/lon
    shp = to_shape(db_ponto.geom)
    return schemas.PontoResponse(
        id=db_ponto.id,
        nome=db_ponto.nome,
        descricao=db_ponto.descricao,
        latitude=shp.y,
        longitude=shp.x
    )


@router.get("/pontos/", response_model=List[schemas.PontoResponse])
def read_points(db: Session = Depends(get_db)):
    pontos = db.query(models.GeometriaPonto).all()
    results = []
    for p in pontos:
        shp = to_shape(p.geom)
        results.append(schemas.PontoResponse(
            id=p.id,
            nome=p.nome,
            descricao=p.descricao,
            latitude=shp.y,
            longitude=shp.x
        ))
    return results

@router.get("/health")
def check_health():
    return {"status": "ready", "database": "PostGIS connected"}