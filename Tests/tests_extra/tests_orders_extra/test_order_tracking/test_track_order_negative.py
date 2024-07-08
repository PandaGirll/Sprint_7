import allure
import pytest

from data.data import EXPECTED_RESPONSES
from data.helpers import ValidationHelper, OrderHelper


@allure.feature('Получение заказа по его номеру')
@allure.story('Негативные сценарии')
class TestGetOrderByTrackNegative:

    @allure.title("Попытка получить заказ без указания номера трека")
    @pytest.mark.negative
    def test_get_order_by_track_without_track(self):
        order_helper = OrderHelper()

        with allure.step('Отправка запроса на получение заказа без трека'):
            response = order_helper.get_order_by_track('')

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_response(
                response,
                [EXPECTED_RESPONSES["get_order_by_track_missing_data_code"]],
                EXPECTED_RESPONSES["get_order_by_track_missing_data_message"]
            ), f"Неожиданный ответ при попытке получить заказ без трека. Код: {response.status_code}, Тело: {response.json()}"

    @allure.title("Попытка получить несуществующий заказ")
    def test_get_non_existent_order_by_track(self):
        order_helper = OrderHelper()
        non_existent_track = 999999999

        with allure.step('Отправка запроса на получение несуществующего заказа'):
            response = order_helper.get_order_by_track(non_existent_track)

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_response(
                response,
                [EXPECTED_RESPONSES["get_order_by_track_not_found_code"]],
                EXPECTED_RESPONSES["get_order_by_track_not_found_message"]
            ), f"Неожиданный ответ при попытке получить несуществующий заказ. Код: {response.status_code}, Тело: {response.json()}"
