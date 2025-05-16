import allure
from conftest import *


class TestOrderCreation:
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized_with_ingredients(self, registered_user):
        _, token = registered_user
        headers = {"Authorization": token}

        ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"]
        ingredient_ids = [item["_id"] for item in ingredients[:2]]

        response = requests.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": ingredient_ids})

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()


    @allure.title("Создание заказа без авторизации с валидными ингредиентами")
    def test_create_order_unauthorized_with_ingredients(self):
        ingredients = requests.get(f"{BASE_URL}/ingredients").json()["data"]
        ingredient_ids = [item["_id"] for item in ingredients[:2]]

        response = requests.post(f"{BASE_URL}/orders", json={"ingredients": ingredient_ids})

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()


    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user):
        _, token = registered_user
        headers = {"Authorization": token}

        response = requests.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": []})

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == "Ingredient ids must be provided"


    @allure.title("Создание заказа с неверным хешом ингредиента")
    def test_create_order_invalid_ingredient_hash(self, registered_user):
        _, token = registered_user
        headers = {"Authorization": token}
        invalid_ingredients = ["invalid_id_123"]

        response = requests.post(f"{BASE_URL}/orders", headers=headers, json={"ingredients": invalid_ingredients})

        assert response.status_code == 500
