from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'not.exist@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        "name": "New User",
        "email": "new.user@mail.com"
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int) #id

    get_response = client.get("/api/v1/user", params={"email": new_user["email"]})
    assert get_response.status_code == 200
    assert get_response.json()["name"] == new_user["name"]
    assert get_response.json()["email"] == new_user["email"]

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_user = users[0]
    response = client.post("/api/v1/user", json={
        "name": "Duplicate",
        "email": existing_user["email"]
    })
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    email = "to.delete@mail.com"
    #создаю
    client.post("/api/v1/user", json={"name": "To Delete", "email": email})

    #удаляю
    delete_response = client.delete("/api/v1/user", params={"email": email})
    assert delete_response.status_code == 204

    get_response = client.get("/api/v1/user", params={"email": email})
    assert get_response.status_code == 404