from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Тестовые данные
test_users = [
    {"id": 1, "name": "Ivan Ivanov", "email": "i.i.ivanov@mail.com"},
    {"id": 2, "name": "Petr Petrov", "email": "p.p.petrov@mail.com"}
]

def test_get_existing_user():
    """Получение существующего пользователя"""
    response = client.get("/api/v1/user", params={"email": test_users[0]["email"]})
    assert response.status_code == 200
    assert response.json() == test_users[0]

def test_get_nonexistent_user():
    """Получение несуществующего пользователя"""
    response = client.get("/api/v1/user", params={"email": "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    """Создание пользователя с уникальной почтой"""
    new_user = {"name": "New User", "email": "new.user@mail.com"}
    response = client.post("/api/v1/user", json=new_user)
    
    assert response.status_code == 201
    assert isinstance(response.json(), int)  # Проверяем что возвращается ID
    
    # Проверяем что пользователь действительно создан
    get_response = client.get("/api/v1/user", params={"email": new_user["email"]})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == new_user["name"]
    assert get_response.json()["email"] == new_user["email"]

def test_create_user_with_invalid_email():
    """Попытка создания пользователя с существующим email"""
    duplicate_user = {"name": "Duplicate", "email": test_users[0]["email"]}
    response = client.post("/api/v1/user", json=duplicate_user)
    
    assert response.status_code == 409  # Изменили с 400 на 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    """Удаление пользователя"""
    # Сначала создаем тестового пользователя
    temp_user = {"name": "Temp User", "email": "temp@mail.com"}
    user_id = client.post("/api/v1/user", json=temp_user).json()
    
    # Удаляем по email (согласно вашему роутеру)
    delete_response = client.delete("/api/v1/user", params={"email": temp_user["email"]})
    assert delete_response.status_code == 204
    
    # Проверяем что пользователь удален
    get_response = client.get("/api/v1/user", params={"email": temp_user["email"]})
    assert get_response.status_code == 404