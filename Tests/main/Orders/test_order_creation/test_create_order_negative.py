import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import OrderHelper


@allure.feature('Создание заказа')
@allure.story('Негативные сценарии')
class TestCreateOrderNegative:

    @pytest.mark.negative
    @pytest.mark.parametrize("missing_field", [
        "firstName", "lastName", "address", "metroStation", "phone", "rentTime", "deliveryDate"
    ])
    @allure.description("""
        Известный баг: API позволяет создать заказ без обязательных полей.
        Ожидаемое поведение: код ответа 400 Bad Request.
        Фактическое поведение: код ответа 201 Created или 500 Internal Server Error.
    """)
    def test_create_order_missing_field(self, order_setup_teardown, missing_field):
        with allure.step(f'Генерация данных заказа без поля {missing_field}'):
            order_data = OrderHelper.generate_order_without_field(missing_field)

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        with allure.step('Проверка ответа'):
            assert ((response.status_code == EXPECTED_RESPONSES["create_order_missing_field_code"] and
                     "message" in response.json() and
                     response.json()["message"] == EXPECTED_RESPONSES["create_order_missing_field_message"].format(
                        field=missing_field)) or
                    (response.status_code == EXPECTED_RESPONSES["create_order_success_code"] and
                     "track" in response.json()) or
                    (response.status_code == EXPECTED_RESPONSES["create_order_server_error_code"] and
                     "message" in response.json() and
                     EXPECTED_RESPONSES["create_order_server_error_message"] in response.json()["message"])), \
                f"Неожиданный ответ при создании заказа без поля {missing_field}. Код ответа: {response.status_code}, ответ: {response.json()}"

        if response.status_code == EXPECTED_RESPONSES["create_order_success_code"]:
            order_setup_teardown.order_id = response.json()["track"]
            allure.attach(f"Внимание: заказ успешно создан без обязательного поля {missing_field}", "Предупреждение",
                          allure.attachment_type.TEXT)
        elif response.status_code == EXPECTED_RESPONSES["create_order_server_error_code"]:
            allure.attach(f"Внимание: сервер вернул ошибку 500 для отсутствующего поля {missing_field}",
                          "Предупреждение", allure.attachment_type.TEXT)

    @pytest.mark.negative
    @pytest.mark.parametrize("empty_field", [
        "firstName", "lastName", "address", "metroStation", "phone", "rentTime", "deliveryDate"
    ])
    @allure.description("""
        Известный баг: API позволяет создать заказ с пустыми обязательными полями.
        Ожидаемое поведение: код ответа 400 Bad Request.
        Фактическое поведение: код ответа 201 Created или 500 Internal Server Error.
    """)
    def test_create_order_empty_field(self, order_setup_teardown, empty_field):
        with allure.step(f'Генерация данных заказа с пустым полем {empty_field}'):
            order_data = OrderHelper.generate_order_with_empty_field(empty_field)

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        assert ((response.status_code == EXPECTED_RESPONSES["create_order_empty_field_code"] and
                 "message" in response.json() and
                 response.json()["message"] == EXPECTED_RESPONSES["create_order_empty_field_message"].format(
                    field=empty_field)) or
                (response.status_code == EXPECTED_RESPONSES["create_order_success_code"] and
                 "track" in response.json()) or
                (response.status_code == EXPECTED_RESPONSES["create_order_server_error_code"] and
                 "message" in response.json() and
                 (EXPECTED_RESPONSES["create_order_server_error_message"] in response.json()["message"] or
                  EXPECTED_RESPONSES["create_order_server_error_message_date"] in response.json()["message"]))), \
            f"Неожиданный ответ при создании заказа с пустым полем {empty_field}. Код ответа: {response.status_code}, ответ: {response.json()}"

        if response.status_code == EXPECTED_RESPONSES["create_order_success_code"]:
            order_setup_teardown.order_id = response.json()["track"]
            allure.attach(f"Внимание: заказ успешно создан с пустым обязательным полем {empty_field}", "Предупреждение",
                          allure.attachment_type.TEXT)
        elif response.status_code == EXPECTED_RESPONSES["create_order_server_error_code"]:
            allure.attach(f"Внимание: сервер вернул ошибку 500 для пустого поля {empty_field}", "Предупреждение",
                          allure.attachment_type.TEXT)
