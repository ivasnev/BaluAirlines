from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

bd_name = "study_demo_medium_test"
bd_port = 5432
bd_user = "study"
bd_password = "study"
postgre_server = "0.0.0.0"
debug = True
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{bd_user}:{bd_password}@{postgre_server}:{bd_port}/{bd_name}"
)
Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
Base.metadata.bind = engine
SessionLocal = sessionmaker(bind=engine, autoflush=False)


# session = Session()

def get_db_test():
    """
    Генератор сессии для контекстного менеджера

    :return: Генератор
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
