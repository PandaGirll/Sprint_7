import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES


@allure.feature('Логин курьера')
@allure.story('Позитивный сценарий')
class TestLoginCourierPositive:

    @pytest.mark.positive
    def test_login_courier_success(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier

        with allure.step('Отправка запроса на логин курьера'):
            response = requests.post(API_ENDPOINTS["login_courier"],
                                     json={"login": courier["login"], "password": courier["password"]})

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_success_code"] and
                    "id" in response.json()), \
                f"Ошибка при логине курьера. Код ответа: {response.status_code}, Тело ответа: {response.json()}"
