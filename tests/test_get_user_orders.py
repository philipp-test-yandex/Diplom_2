from conftest import *
import requests
import allure
from helpers.constants import BASE_URL, UNAUTHORIZED_ERROR_MESSAGE


@allure.epic("Заказ")
@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized_user(self, registered_user):
        _, token = registered_user
        headers = {"Authorization": token}

        ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"]
        ingredient_ids = [item["_id"] for item in ingredients[:2]]

        requests.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": ingredient_ids})

        response = requests.get(f"{BASE_URL}/orders", headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["orders"], list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized_user(self):
        response = requests.get(f"{BASE_URL}/orders")

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == UNAUTHORIZED_ERROR_MESSAGE
