import allure
import pytest

from data.data import EXPECTED_RESPONSES
from data.helpers import OrderHelper, ValidationHelper


@allure.feature('Принятие заказа')
@allure.story('Негативные сценарии')
class TestAcceptOrderNegative:

    @pytest.mark.negative
    @allure.title("Попытка принять заказ с несуществующим id заказа")
    def test_accept_order_non_existent_order(self, order_and_courier_setup):
        (_, courier_id) = order_and_courier_setup
        non_existent_order_id = 999999999

        with allure.step('Отправка запроса на принятие несуществующего заказа'):
            response = OrderHelper.accept_order(non_existent_order_id, courier_id)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_response(
                response,
                [EXPECTED_RESPONSES["accept_order_not_found_order_code"]],
                EXPECTED_RESPONSES["accept_order_not_found_order_message"]
            ), f"Неожиданный ответ при попытке принять несуществующий заказ. Код: {response}"

    @pytest.mark.negative
    @allure.title("Попытка принять заказ с несуществующим id курьера")
    def test_accept_order_non_existent_courier(self, order_and_courier_setup):
        (order_id, _) = order_and_courier_setup
        non_existent_courier_id = 999999999

        with allure.step('Отправка запроса на принятие заказа несуществующим курьером'):
            response = OrderHelper.accept_order(order_id, non_existent_courier_id)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_response(
                response,
                [EXPECTED_RESPONSES["accept_order_not_found_courier_code"]],
                EXPECTED_RESPONSES["accept_order_not_found_courier_message"]
            ), f"Неожиданный ответ при попытке принять заказ несуществующим курьером. Код: {response.status_code}, Тело: {response.json()}"

    @pytest.mark.negative
    @allure.title("Попытка принять уже принятый заказ")
    def test_accept_already_accepted_order(self, order_and_courier_setup):
        order_id, courier_id = order_and_courier_setup

        with allure.step('Принятие заказа в первый раз'):
            OrderHelper.accept_order(order_id, courier_id)

        with allure.step('Попытка принять уже принятый заказ'):
            response = OrderHelper.accept_order(order_id, courier_id)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_response(
                response,
                [EXPECTED_RESPONSES["accept_order_conflict_code"]],
                EXPECTED_RESPONSES["accept_order_conflict_message"]
            ), f"Неожиданный ответ при попытке принять уже принятый заказ. Код: {response.status_code}, Тело: {response.json()}"
