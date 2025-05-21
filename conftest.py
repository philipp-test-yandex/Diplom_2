import pytest
import requests
from helpers.constants import BASE_URL
from helpers.data import DEFAULT_PASSWORD, DEFAULT_NAME
from helpers.utils import generate_unique_email



@pytest.fixture
def new_user():
    user = {
        "email": generate_unique_email(),
        "password": DEFAULT_PASSWORD,
        "name": DEFAULT_NAME
    }
    yield user

    token_resp = requests.post(f"{BASE_URL}/auth/login", json=user)
    if token_resp.ok:
        token = token_resp.json()["accessToken"]
        headers = {"Authorization": token}
        requests.delete(f"{BASE_URL}/auth/user", headers=headers)


@pytest.fixture
def registered_user(new_user):
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)
    assert response.status_code == 200, "Регистрация не удалась"
    token = response.json()["accessToken"]

    yield new_user, token

    headers = {"Authorization": token}
    requests.delete(f"{BASE_URL}/auth/user", headers=headers)
