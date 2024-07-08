import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import ValidationHelper


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
            assert ValidationHelper.validate_response(response,
                                                      [EXPECTED_RESPONSES["get_orders_list_courier_not_found_code"],
                                                       EXPECTED_RESPONSES["get_orders_list_bad_request_code"]],
                                                      [EXPECTED_RESPONSES[
                                                           "get_orders_list_courier_not_found_message"].format(999999),
                                                       EXPECTED_RESPONSES["get_orders_list_bad_request_message"]]), \
                f"Неожиданный ответ при получении заказов с некорректным ID курьера. Код ответа: {response.status_code}, ответ: {response.json()}"

    @pytest.mark.negative
    @allure.title("Получение заказов с некорректной станцией метро")
    def test_get_orders_with_invalid_station(self):
        with allure.step('Отправка запроса на получение заказов с некорректной станцией метро'):
            params = {"nearestStation": "[500]"}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_response(response,
                                                      [EXPECTED_RESPONSES["get_orders_list_success_code"],
                                                       EXPECTED_RESPONSES["get_orders_list_bad_request_code"]],
                                                      [EXPECTED_RESPONSES["get_orders_list_success_response"],
                                                       EXPECTED_RESPONSES["get_orders_list_bad_request_message"]]), \
                f"Неожиданный ответ при получении заказов с некорректной станцией метро. Код ответа: {response.status_code}, ответ: {response.json()}"

    @pytest.mark.negative
    @allure.title("Получение заказов с отрицательным значением limit")
    def test_get_orders_with_negative_limit(self):
        with allure.step('Отправка запроса на получение заказов с отрицательным значением limit'):
            params = {"limit": -1}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_response(response,
                                                      [EXPECTED_RESPONSES["get_orders_list_bad_request_code"]],
                                                      [EXPECTED_RESPONSES["get_orders_list_bad_request_message"]]), \
                f"Неожиданный ответ при получении заказов с отрицательным значением limit. Код ответа: {response.status_code}, ответ: {response.json()}"

    @pytest.mark.negative
    @allure.title("Получение заказов с отрицательным значением page")
    def test_get_orders_with_negative_page(self):
        with allure.step('Отправка запроса на получение заказов с отрицательным значением page'):
            params = {"page": -1}
            response = requests.get(API_ENDPOINTS["list_orders"], params=params)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_response(response,
                                                      [EXPECTED_RESPONSES["get_orders_list_bad_request_code"]],
                                                      [EXPECTED_RESPONSES["get_orders_list_bad_request_message"]]), \
                f"Неожиданный ответ при получении заказов с отрицательным значением page. Код ответа: {response.status_code}, ответ: {response.json()}"