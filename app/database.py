from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurações do banco
DATABASE_URL =  "postgresql://postgres:123@db:5432/geodb"

# Preparar o Pool de conexões
engine = create_engine(DATABASE_URL)

# Cria a classe de sessãoso
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Variável para "guardar" as tabelas de geometrias
Base = declarative_base()

# Função para pegar a sessão do banco
def get_db():
    db = SessionLocal() # A classe de sessão é instanciada
    try:
        # yield espera uma resposta HTTP para retornar para a função, ao contrário do return
        yield db
    finally:
        db.close()