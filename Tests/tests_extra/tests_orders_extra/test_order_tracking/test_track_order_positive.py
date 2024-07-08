import time
import logging
import pytest
import allure
from data.data import EXPECTED_RESPONSES
from data.helpers import ValidationHelper, OrderHelper


@pytest.mark.positive
class TestGetOrderByTrackPositive:

    @allure.title("Успешное получение заказа по номеру трека")
    def test_get_order_by_track_success(self, setup_and_teardown_order_with_track):
        order_helper = OrderHelper()
        order_track = setup_and_teardown_order_with_track

        with allure.step('Отправка запроса на получение несуществующего заказа'):
            response = order_helper.get_order_by_track(order_track)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_with_order(
                response,
                EXPECTED_RESPONSES["get_order_by_track_success_code"],
            ), f"Неожиданный ответ при попытке получить информацию о заказе. Код: {response.status_code}, Тело: {response.json()}"
