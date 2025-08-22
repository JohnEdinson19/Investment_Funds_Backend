import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_register_success():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "phone": "1234567890",
        "notification": True,
        "role": "user"
    }
    
    response = client.post("/register", json=user_data)
    
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_register_user_exists():
    user_data = {
        "username": "existinguser",
        "email": "existinguser@example.com",
        "password": "testpassword",
        "phone": "1234567890",
        "notification": True,
        "role": "user"
    }
    
    # Primero, registra al usuario
    client.post("/register", json=user_data)
    
    # Luego intenta registrarlo de nuevo
    response = client.post("/register", json=user_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Usuario ya existe"

@pytest.mark.asyncio
async def test_login_success():
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "loginpassword",
        "phone": "1234567890",
        "notification": True,
        "role": "user"
    }
    
    # Registra el usuario
    client.post("/register", json=user_data)
    
    # Intenta iniciar sesión
    response = client.post("/login", data={"username": user_data["username"], "password": user_data["password"]})
    
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    response = client.post("/login", data={"username": "invaliduser", "password": "wrongpassword"})
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"
