import pytest
import requests
from helpers.constants import BASE_URL

@pytest.fixture
def new_user():
    user = {
        "email": generate_unique_email(),
        "password": "Test123",
        "name": "Test User"
    }
    yield user
    token_resp = requests.post(f"{BASE_URL}/auth/login", json=user)
    if token_resp.ok:
        token = token_resp.json()["accessToken"]
        headers = {"Authorization": token}
        requests.delete(f"{BASE_URL}/auth/user", headers=headers)

counter = 0
def generate_unique_email():
    global counter
    counter += 1
    return f"user{counter}@test.com"


@pytest.fixture
def registered_user(new_user):
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)
    token = response.json()["accessToken"]
    yield new_user, token

    headers = {"Authorization": token}
    requests.delete(f"{BASE_URL}/auth/user", headers=headers)