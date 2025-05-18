import requests


BASE_URL = "http://localhost:5000"


def register(username, password, role):
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "password": password,
        "roles": role
    })
    print("Register:", response.json())

def login(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    print("Login:", response.json())
    return response.json()

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

def refresh(old_token):
    headers = {"Authorization": f"Bearer {old_token}"}
    response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)
    print("Refresh:", response.json())

def read_data(token, page, limit, filters):
    headers = {"Authorization": f"Bearer {token}"}
    headers["X-API-Version"] = "v1"
    params = {
            "page": page,
            "limit": limit
        }
    json_body = {
        "filters": filters
    }
    response = requests.get(
        f"{BASE_URL}/data/raw-scrap-data",
        params = params, 
        headers = headers,
        json = json_body)
    response.raise_for_status()
    print("Response:", response.json())

def create_data(token, data):
    headers = {"Authorization": f"Bearer {token}"}
    headers["X-API-Version"] = "v1"
    headers["Content-Type"]= "application/json"
    response = requests.post(
        f"{BASE_URL}/data/raw-scrap-data",
        headers = headers,
        json = data,
    )
    response.raise_for_status()
    print("Response:", response.json())

def delete_data(token, filters):
    headers = {"Authorization": f"Bearer {token}"}
    headers["X-API-Version"] = "v1"
    params = filters
    response = requests.delete(f"{BASE_URL}/data/raw-scrap-data",params = params, headers = headers)
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
    # register(username, password, role)
    token = login(username, password)
    # token = update(token.get("access_token"), username, password, update_data_1)
    # token = update(token.get("access_token"), username, password, update_data_2)
    if token:
        access_token = token.get("access_token")
        refresh_token = token.get("refresh_token")
        # refresh(refresh_token)
        sample_read_filters = {
            "and": {
                "name": {
                    "like": ["%Sampo%", "%Sabun%"]
                },
                "and" : {
                    "price_gte": 100000,
                    "price_lte": 500000,
                },
                "or": {
                    "originalprice_gt": 10000,
                    "discountpercentage_gte": 5.0,
                    "platform": {
                        "in": ["tokopedia", "blibli"]
                    },
                },
            },
        }  
        read_data(token = access_token, page = 1, limit = 5, filters = sample_read_filters)
        # sample_insert_data = {
        #     "name": "bla-bla-bla",
        #     "price": 200000,
        #     "platform": "tokopedia",
        #     "createdate": "2025-05-17"
        # }
        # create_data(token = access_token, data = sample_insert_data)
        # sample_delete_data = {
        #     "id": 10
        # }
        # delete_data(token = access_token, filters = sample_delete_data)
        