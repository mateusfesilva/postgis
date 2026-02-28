from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from .database import Base

class GeometriaPonto(Base):
    __tablename__ = "pontos_interesse"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    # (WGS84 - Lat/Lon)
    geom = Column(Geometry("POINT", srid=4326))
