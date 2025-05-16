import allure
from conftest import *
from helpers.constants import *

class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, new_user):
        response = requests.post(f"{BASE_URL}/auth/register", json=new_user)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Регистрация с повторным email")
    def test_create_user_dublicat_email(self, new_user):
        requests.post(f"{BASE_URL}/auth/register", json=new_user)
        response = requests.post(f"{BASE_URL}/auth/register", json=new_user)
        assert response.status_code == 403
        assert response.json()["message"] == USER_ALREADY_EXISTS

    @pytest.mark.parametrize("field", ["email", "password", "name"])
    @allure.title("Регистрация без обязательного поля: {field}")
    def test_register_missing_required_field(self, field, new_user):
        user_data = new_user.copy()
        user_data.pop(field)
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        assert response.status_code == 403
        assert response.json()["message"] == MISSING_REQUIRED_FIELDS