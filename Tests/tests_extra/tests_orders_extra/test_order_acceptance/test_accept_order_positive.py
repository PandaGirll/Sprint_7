import pytest
import allure
import requests
from data.data import EXPECTED_RESPONSES
from data.helpers import OrderHelper, ValidationHelper


@allure.feature('Принятие заказа')
@allure.story('Позитивные сценарии')
@pytest.mark.positive
class TestAcceptOrderPositive:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, order_and_courier_setup):
        order_id, courier_id = order_and_courier_setup

        with allure.step('Отправка запроса на принятие заказа'):
            response = OrderHelper.accept_order(order_id, courier_id)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_response(
                response,
                [EXPECTED_RESPONSES["accept_order_success_code"]],
                [EXPECTED_RESPONSES["accept_order_success_response"]]
            ), f"Неожиданный ответ при принятии заказа. Код: {response.status_code}, Тело: {response.json()}"
