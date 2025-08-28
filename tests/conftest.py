import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app, get_session
from app.models.user import User
from app.config import settings


# Create a new engine for the test database
engine = create_engine(
    settings.TEST_DATABASE_URL, connect_args={}
)


# Override the get_session dependency to use the test database
def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(name="client")
def client_fixture():
    # Create the database and tables before each test
    SQLModel.metadata.create_all(engine)

    # Yield the TestClient instance
    yield TestClient(app)

    # Drop the database tables after each test
    SQLModel.metadata.drop_all(engine)
