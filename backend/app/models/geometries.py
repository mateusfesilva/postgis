from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from ..core.database import Base


class PointGeometry(Base):
    __tablename__ = "points_geometry"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    # (WGS84 - Lat/Lon)
    geom = Column(Geometry("POINT", srid=4326))

class PolygonGeometry(Base):
    __tablename__ = "polygons_geometry"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    # (WGS84 - Lat/Lon)
    geom = Column(Geometry("POLYGON", srid=4326))