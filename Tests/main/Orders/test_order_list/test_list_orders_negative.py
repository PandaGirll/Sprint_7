import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES


@allure.feature('Получение списка заказов')
@allure.story('Негативные сценарии')
class TestListOrdersNegative:

    @pytest.mark.negative
    @allure.title("Получение заказов с некорректным ID курьера")
    def test_get_orders_with_invalid_courier_id(self):
        with allure.step('Отправка запроса на получение заказов с некорректным ID курьера'):
            params = {"courierId": 999999}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_courier_not_found_code"] or \
                   response.status_code == 500, \
                f"Неожиданный ответ при получении заказов с некорректным ID курьера. Код ответа: {response.status_code}, ответ: {response.json()}"

        if response.status_code == 500:
            allure.attach("Сервер вернул ошибку 500", "Предупреждение", allure.attachment_type.TEXT)

    @pytest.mark.negative
    @allure.title("Получение заказов с некорректной станцией метро")
    def test_get_orders_with_invalid_station(self):
        with allure.step('Отправка запроса на получение заказов с некорректной станцией метро'):
            params = {"nearestStation": "[]"}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_success_code"] or \
                   response.status_code == EXPECTED_RESPONSES["get_orders_list_bad_request_code"], \
                f"Неожиданный ответ при получении заказов с некорректной станцией метро. Код ответа: {response.status_code}, ответ: {response.json()}"

        if response.status_code == 500:
            allure.attach("Сервер вернул ошибку 500", "Предупреждение", allure.attachment_type.TEXT)

    @pytest.mark.negative
    @allure.title("Получение заказов с отрицательным значением limit")
    def test_get_orders_with_negative_limit(self):
        with allure.step('Отправка запроса на получение заказов с отрицательным значением limit'):
            params = {"limit": -1}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_bad_request_code"], \
                f"Неожиданный ответ при получении заказов с отрицательным значением limit. Код ответа: {response.status_code}, ответ: {response.json()}"

    @pytest.mark.negative
    @allure.title("Получение заказов с отрицательным значением page")
    def test_get_orders_with_negative_page(self):
        with allure.step('Отправка запроса на получение заказов с отрицательным значением page'):
            params = {"page": -1}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert response.status_code == EXPECTED_RESPONSES["get_orders_list_bad_request_code"], \
                f"Неожиданный ответ при получении заказов с отрицательным значением page. Код ответа: {response.status_code}, ответ: {response.json()}"
