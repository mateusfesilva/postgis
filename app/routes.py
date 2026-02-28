from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from typing import List
from . import models, schemas
from .database import get_db

router = APIRouter()

# Organiza os paths dos endpoints (e agrupa no swagger)
@router.post("/points/", response_model=schemas.PointResponse)
def create_point(point: schemas.CreatePoint, db: Session = Depends(get_db)):
    # lat/len para WKT
    wkt_element = f"POINT({point.lon} {point.lat})"

    db_point = models.PointGeometry(
        name=point.name,
        description=point.description,
        geom=wkt_element
    )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)

    # Geom para lat/lon
    shp = to_shape(db_point.geom)
    return schemas.PointResponse(
        id=db_point.id,
        name=db_point.name,
        description=db_point.description,
        lat=shp.y,
        lon=shp.x
    )


@router.get("/points/", response_model=List[schemas.PointResponse])
def read_points(db: Session = Depends(get_db)):
    points = db.query(models.PointGeometry).all()
    results = []
    for p in points:
        shp = to_shape(p.geom)
        results.append(schemas.PointResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            lat=shp.y,
            lon=shp.x
        ))
    return results

@router.get("/health")
def check_health():
    return {"status": "ready", "database": "PostGIS connected"}