import allure
from helpers.constants import *
from conftest import *


class TestUserLogin:
    @allure.title("Логин под существующим пользователем")
    def test_login_success(self, registered_user):
        user, _ = registered_user

        with allure.step("Отправляем POST запрос на логин"):
            response = requests.post(f"{BASE_URL}/auth/login", json=user)

        with allure.step("Проверяем статус и токен"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.title("Логин с неверными данными")
    @pytest.mark.parametrize("email, password", [
        ("wrongemail@test.com", "Test123"),
        ("", "Test123"),
        ("user@test.com", "wrongpass"),
        ("user@test.com", ""),
    ])
    def test_login_with_invalid_credentials(self, email, password):
        with allure.step("Отправляем POST запрос с невалидными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
            })

        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["message"] == LOGIN_ERROR_MESSAGE
