import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Arithmetic API v2" in response.data

def test_add(client):
    response = client.get('/add?x=5&y=3')
    assert response.status_code == 200
    assert response.get_json()["result"] == 8

def test_subtract(client):
    response = client.get('/subtract?x=10&y=4')
    assert response.status_code == 200
    assert response.get_json()["result"] == 6

def test_multiply(client):
    response = client.get('/multiply?x=2&y=5')
    assert response.status_code == 200
    assert response.get_json()["result"] == 10

def test_divide(client):
    response = client.get('/divide?x=10&y=2')
    assert response.status_code == 200
    assert response.get_json()["result"] == 5

def test_divide_by_zero(client):
    response = client.get('/divide?x=10&y=0')
    assert response.status_code == 400
    assert "error" in response.get_json()
