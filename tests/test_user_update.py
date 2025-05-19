import allure
from helpers.constants import *
from conftest import *


class TestUserUpdate:
    @allure.title("Изменение имени пользователя с авторизацией")
    def test_update_name_authorized(self, registered_user):
        user, token = registered_user
        headers = {"Authorization": token}

        with allure.step("Отправляем PATCH с новым именем"):
            response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json={"name": "Updated Name"})

        assert response.status_code == 200
        assert response.json()["user"]["name"] == "Updated Name"

    @allure.title("Изменение email пользователя с авторизацией")
    def test_update_email_authorized(self, registered_user):
        user, token = registered_user
        headers = {"Authorization": token}
        new_email = user["email"].replace("@", "+updated@")

        response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json={"email": new_email})

        assert response.status_code == 200
        assert response.json()["user"]["email"] == new_email

    @allure.title("Изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("field, value", [ ("name", "Unauthorized Name"), ("email", "unauth@example.com"),])
    def test_update_user_unauthorized(self, field, value):
        payload = {field: value}

        response = requests.patch(f"{BASE_URL}/auth/user", headers={}, json=payload)

        assert response.status_code == 401
        assert response.json()["message"] == UNAUTHORIZED_ERROR_MESSAGE
