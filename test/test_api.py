from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app, Base, get_db
import pytest


# Setup the TestClient
client = TestClient(app)

# Setup the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture()  # Use @pytest.fixture() for setup_db
def setup_db():
    Base.metadata.create_all(bind=engine)  # Create tables directly in setup_db
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_item(setup_db):
    #setup()
    response = client.post(
        "/items/", json={"name": "Test Item", "price": 99.90, "description": "This is a test item"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 99.90
    assert data["description"] == "This is a test item"
    assert "id" in data


def test_read_item():
    setup()
    # Create an item
    response = client.post(
        "/items/", json={"name": "Test Item", "price": 99.90, "description": "This is a test item"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = data["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 99.90
    assert data["description"] == "This is a test item"
    assert data["id"] == item_id


def test_update_item():
    setup()
    item_id = 1
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Test Item", "price": 99.90, "description": "This is a test item"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 99.90
    assert data["description"] == "This is a test item"
    assert data["id"] == item_id


def test_delete_item():
    setup()
    item_id = 1
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == item_id
    # Try to get the deleted item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404, response.text


def setup() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)

# @pytest.fixture()
# def setup_db():
#     setup()
#     yield
#     teardown()
