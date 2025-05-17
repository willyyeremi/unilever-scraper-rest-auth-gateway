import requests

BASE_URL = "http://localhost:5000"

# 1. Register user
def register(username, password, role):
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "password": password,
        "roles": role
    })
    print("Register:", response.json())

# 2. Login user
def login(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    print("Login:", response.json())
    return response.json()

# 3. Update token
def update(access_token, username, password, update_data):
    json_body = {
        "username": username,
        "password": password
    }
    json_body.update(update_data)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/auth/update", headers = headers, json = json_body)
    print("Update:", response.json())
    return response.json()

# 4. Refresh token
def refresh(old_token):
    headers = {"Authorization": f"Bearer {old_token}"}
    response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)
    print("Refresh:", response.json())

# 5. Access protected endpoint
def access_protected(token, page, limit, **kwargs):
    headers = {"Authorization": f"Bearer {token}"}
    params = {
            "page": page,
            "limit": limit
        }
    params.update(kwargs)
    response = requests.get(f"{BASE_URL}/data/raw-scrap-data",params = params, headers = headers)
    response.raise_for_status()
    print("Response:", response.json())

if __name__ == "__main__":
    username = "admin"
    password = "admin"
    role = "admin"
    update_data_1 = {
        "username_update": "admin_update",
        "is_active_update": "0"
    }
    update_data_2 = {
        "password_update": "admin_update",
        "is_active_update": "1"
    }

    register(username, password, role)
    token = login(username, password)
    token = update(token.get("access_token"), username, password, update_data_1)
    token = update(token.get("access_token"), username, password, update_data_2)
    if token:
        access_token = token.get("access_token")
        refresh_token = token.get("refresh_token")
        refresh(refresh_token)
        access_protected(token = access_token, page = 1, limit = 5, id = 1)
