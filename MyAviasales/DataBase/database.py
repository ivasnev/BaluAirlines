from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

bd_name = "study_demo_medium"
bd_port = 5432
bd_user = "study"
bd_password = "study"
postgre_server = "0.0.0.0"
debug = True
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{bd_user}:{bd_password}@{postgre_server}:{bd_port}/{bd_name}"
)
Base = declarative_base()
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=debug)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=debug)
Base.metadata.bind = engine

# SessionLocal = sessionmaker(bind=engine, autoflush=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession,
                            autoflush=False, expire_on_commit=False)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
