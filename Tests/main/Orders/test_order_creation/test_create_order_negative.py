import pytest
import allure
import requests
from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.test_data_generator import generate_order_data
from data.helpers import OrderHelper


@allure.feature('Создание заказа')
@allure.story('Негативные сценарии')
class TestCreateOrderNegative(OrderHelper):

    @pytest.mark.negative
    @pytest.mark.parametrize("missing_field", [
        "firstName", "lastName", "address", "metroStation", "phone", "rentTime", "deliveryDate"
    ])
    @allure.description("""
        Известный баг: API позволяет создать заказ без обязательных полей.
        Ожидаемое поведение: код ответа 400 Bad Request.
        Фактическое поведение: код ответа 201 Created.
    """)
    def test_create_order_missing_field(self, missing_field):
        with allure.step(f'Генерация данных заказа без поля {missing_field}'):
            order_data = generate_order_data()
            del order_data[missing_field]

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_order_missing_field_code"] and
                    "message" in response.json() and
                    response.json()["message"] == EXPECTED_RESPONSES["create_order_missing_field_message"].format(
                        field=missing_field)), \
                f"Ошибка при создании заказа без поля {missing_field}. Код ответа: {response.status_code}, ответ: {response.json()}"

    @pytest.mark.negative
    @pytest.mark.parametrize("empty_field", [
        "firstName", "lastName", "address", "metroStation", "phone", "rentTime", "deliveryDate"
    ])
    @allure.description("""
        Известный баг: API позволяет создать заказ без обязательных полей.
        Ожидаемое поведение: код ответа 400 Bad Request.
        Фактическое поведение: код ответа 201 Created.
    """)
    def test_create_order_empty_field(self, empty_field):
        with allure.step(f'Генерация данных заказа с пустым полем {empty_field}'):
            order_data = generate_order_data()
            order_data[empty_field] = ""

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_order_empty_field_code"] and
                    "message" in response.json() and
                    response.json()["message"] == EXPECTED_RESPONSES["create_order_empty_field_message"].format(
                        field=empty_field)), \
                f"Ошибка при создании заказа с пустым полем {empty_field}. Код ответа: {response.status_code}, ответ: {response.json()}"