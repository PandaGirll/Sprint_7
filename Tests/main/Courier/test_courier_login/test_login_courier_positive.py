import pytest
import allure
import requests
from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import CourierHelper


@allure.feature('Логин курьера')
@allure.story('Позитивные сценарии')
class TestLoginCourierPositive(CourierHelper):

    @pytest.mark.positive
    def test_courier_login_success(self):
        with allure.step('Отправка запроса на логин курьера'):
            response = requests.post(API_ENDPOINTS["login_courier"], json={
                "login": self.courier_data["login"],
                "password": self.courier_data["password"]
            })

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_success_code"] and
                    "id" in response.json()), \
                f"Ошибка при логине курьера. Код ответа: {response.status_code}, тело ответа: {response.json()}"
