import requests

BASE_URL = "http://localhost:5000/auth"

# 1. Register user
def register(username, password):
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password
    })
    print("Register:", response.json())

# 2. Login user
def login(username, password):
    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
    print("Login:", response.json())
    return response.json().get("access_token")

# 3. Access protected endpoint
def access_protected(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/protected", headers=headers)
    print("Protected:", response.json())

if __name__ == "__main__":
    username = "user1"
    password = "secret123"

    register(username, password)
    token = login(username, password)
    if token:
        access_protected(token)
