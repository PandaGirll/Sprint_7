import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import ValidationHelper


@allure.feature('Удаление курьера')
@allure.story('Позитивные сценарии')
class TestDeleteCourierPositive:

    @pytest.mark.positive
    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, courier_for_deletion):
        courier_id = courier_for_deletion

        with allure.step('Отправка запроса на удаление курьера'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id))

        with allure.step('Проверка ответа'):
            assert ValidationHelper.validate_order_response(
                response,
                [EXPECTED_RESPONSES["delete_courier_success_code"]],
                [EXPECTED_RESPONSES["delete_courier_success_response"]]
            ), f"Неожиданный ответ при удалении курьера. Код ответа: {response.status_code}, ответ: {response.json()}"
