from pydantic import Field, field_validator, BaseModel
from typing import List, Tuple
from typing_extensions import Annotated

Lon = Annotated[float, Field(ge=-180.0, le=180.0, description="Longitude.")]
Lat = Annotated[float, Field(ge=-90.0, le=90.0 , description="Latitude.")]
Coordinate = Tuple[Lon, Lat]
LinearRing = List[Coordinate]
PolygonCoordinates = List[LinearRing]

class PolygonGeometry(BaseModel):
    type: str = Field(default="Polygon", pattern="^Polygon$")
    coordinates: PolygonCoordinates

    model_config = {"from_attributes": True}
    # coordinates é passado como parâmetro (rings)
    @field_validator('coordinates')
    def validate_polygon_coordinates(cls, rings):
        for ring in rings:
            if len(ring) < 4:
                raise ValueError("Um LinearRing deve conter pelo menos 4 coordenadas.")
            
            if ring[0] != ring[-1]:
                raise ValueError("O primeiro e o último ponto de um LinearRing devem ser iguais.")
            
        return rings

class CreatePolygon(BaseModel):
    name: str = Field(..., description="Nome do polígono")
    category: str | None = Field(None, description="Categoria do polígono")
    geometry: PolygonGeometry

    # Exemplo de configuração para documentação automática do OpenAPI
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Área de Preservação",
                    "category": "Ambiental",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-46.5333, -23.6667],
                                [-46.5000, -23.6667],
                                [-46.5000, -23.6800],
                                [-46.5333, -23.6800],
                                [-46.5333, -23.6667]
                            ]
                        ]
                    }
                }
            ]
        }
    }

class PointGeometry(BaseModel):
    type: str = Field(default="Point", pattern="^Point$")
    coordinates: Coordinate

class CreatePoint(BaseModel):
    name: str = Field(..., description="Nome do ponto")
    description: str = Field(..., description="Descrição do ponto")
    geometry: PointGeometry

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Estação Barra Funda",
                    "description": "Estação de metrô e terminal de ônibus localizada na zona oeste de São Paulo.",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-46.66735562699073, -23.525530381762763]
                    }
                }
            ]
        }
    }

class PointResponse(BaseModel):
    id: int
    description: str = Field(..., description="Descrição do ponto")
    coordinates: Coordinate
    model_config = {"from_attributes": True}

class PolygonResponse(BaseModel):
    id: int
    name: str = Field(..., description="Nome do polígono")
    category: str | None = Field(None, description="Categoria do polígono")
    geometry: PolygonGeometry
    model_config = {"from_attributes": True}