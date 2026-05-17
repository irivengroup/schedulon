from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from schedulon.infrastructure.config.settings import Settings

settings = Settings()
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database() -> dict:
    try:
        with engine.connect() as conn:
            value = conn.execute(text("select 1")).scalar_one()
        return {"status": "READY", "select_1": value}
    except Exception as exc:
        return {"status": "ERROR", "detail": str(exc)}
