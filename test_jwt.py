import pytest
from server import app
import jwt

SECRET_KEY = "secret123"

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_generate_token(client):
    res = client.post("/generate", data={"user_id": "1"})
    assert res.status_code == 200
    assert "token" in res.json


def test_verify_valid_token(client):
    # first create a token
    token = jwt.encode({"user_id": "1"}, SECRET_KEY, algorithm="HS256")

    res = client.post("/verify", data={"token": token})
    assert res.status_code == 200
    assert res.json["valid"] == True


def test_verify_invalid_token(client):
    res = client.post("/verify", data={"token": "BADTOKEN"})
    assert res.status_code == 401
    assert res.json["valid"] == False
