from pydantic import BaseModel

# Validação do payload de criação de ponto
class CriarPonto(BaseModel):
    nome: str
    descricao: str
    latitude: float
    longitude: float

# Validação do response do servidor
class PontoResponse(BaseModel):
    id: int
    descricao: str
    latitude: float
    longitude: float

class CriarPoligono(BaseModel):
    nome: str
    descricao: str
    coordenadas: list

class Config:
    # Com essa config o pydantic consegue ler os campos no formato de um atributo ao invés de um objeto python
    from_attributes = True

        