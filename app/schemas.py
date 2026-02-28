from pydantic import BaseModel

# Validação do payload de criação de ponto
class CreatePoint(BaseModel):
    name: str
    description: str
    lat: float
    lon: float

# Validação do response do servidor
class PointResponse(BaseModel):
    id: int
    description: str
    lat: float
    lon: float

class CreatePolygon(BaseModel):
    name: str
    description: str
    coords: list

class Config:
    # Com essa config o pydantic consegue ler os campos no formato de um atributo ao invés de um objeto python
    from_attributes = True

        