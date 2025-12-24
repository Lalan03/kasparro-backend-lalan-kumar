from core.database import init_engine, get_engine, get_sessionmaker
from core.models import Base

@pytest.fixture(scope="function")
def db():
    init_engine()
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    SessionLocal = get_sessionmaker()
    session = SessionLocal()
    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)
