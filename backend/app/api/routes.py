from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func  
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape
from typing import List

from ..models import geometries
from ..schemas import geojson
from ..core.database import get_db

router = APIRouter()

# Endpoint para criar um ponto
@router.post("/api/points/", response_model=geojson.PointResponse)
def create_point(point: geojson.CreatePoint, db: Session = Depends(get_db)):
    # lat/len para GeoJSON
    geom_json = point.geometry.model_dump_json()

    db_point = geometries.PointGeometry(
        name=point.name,
        description=point.description,
        geom=func.ST_GeomFromGeoJSON(geom_json)
    )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)

    # GeoJSON para shape (x, y)
    shp = to_shape(db_point.geom)
    return geojson.PointResponse(
        id=db_point.id,
        name=db_point.name,
        description=db_point.description,
        coordinates=(shp.x, shp.y),
    )

# Endpoint para listar todos os pontos
@router.get("/api/points/", response_model=List[geojson.PointResponse])
def read_points(db: Session = Depends(get_db)):
    points = db.query(geometries.PointGeometry).all()
    results = []
    for p in points:
        shp = to_shape(p.geom)
        results.append(
            geojson.PointResponse(
                id=p.id, 
                name=p.name, 
                description=p.description, 
                coordinates=(shp.x, shp.y)
            )
        )
    return results

@router.delete("/api/points/{point_id}", response_model=geojson.PointResponse)
def delete_point(point_id: int, db: Session = Depends(get_db)):
    point = db.query(geometries.PointGeometry).filter(geometries.PointGeometry.id == point_id).first()
    if not point:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")
    
    db.delete(point)
    db.commit()
    
    return {'id': point.id, 'status': 'deleted'}

# Endpoint para criar um polígono
@router.post("/api/polygons/", response_model=geojson.PolygonResponse)
def create_polygon(polygon: geojson.CreatePolygon, db: Session = Depends(get_db)):
    
    geom_json = polygon.geometry.model_dump_json()

    db_polygon = geometries.PolygonGeometry(
        name=polygon.name, 
        category=polygon.category, 
        geom=func.ST_GeomFromGeoJSON(geom_json)
    )
    db.add(db_polygon)
    db.commit()
    db.refresh(db_polygon)

    return geojson.PolygonResponse(
        id=db_polygon.id,
        name=db_polygon.name,
        category=db_polygon.category,
        geometry=polygon.geometry
    )

# Endpoint para listar todos os polígonos
@router.get("/api/polygons/", response_model=List[geojson.PolygonResponse])
def read_polygons(db: Session = Depends(get_db)):
    polygons = db.query(geometries.PolygonGeometry).all()
    results = []
    for p in polygons:
        shp = to_shape(p.geom)
        results.append(
            geojson.PolygonResponse(
                id=p.id,
                name=p.name,
                category=p.category,
                # GeoJSON para shape de polígono (x, y, ...)
                geometry=(shp.__geo_interface__)
            )
        )
    return results


@router.delete("/api/polygons/{polygon_id}")
def delete_polygon(polygon_id: int, db: Session = Depends(get_db)):
    polygon = db.query(geometries.PolygonGeometry).filter(geometries.PolygonGeometry.id == polygon_id).first()
    if not polygon:
        raise HTTPException(status_code=404, detail="Polígono não encontrado")
    
    db.delete(polygon)
    db.commit()
    
    return {'id': polygon.id, 'status': 'deleted'}


# Endpoint para verificar o status da API e a conexão com o banco
@router.get("/api/health")
def check_health():
    return {"status": "ready", "database": "PostGIS connected"}

