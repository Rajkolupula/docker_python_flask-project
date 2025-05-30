import pytest
from app import app

@pytest.fixture
def client():
    # Flask provides a test client for testing routes
    with app.test_client() as client:
        yield client

def test_hello(client):
    # Send GET request to "/"
    response = client.get("/")
    # Check the response data and status code
    assert response.status_code == 200
    assert response.data == b"Flask inside Docker!!"
