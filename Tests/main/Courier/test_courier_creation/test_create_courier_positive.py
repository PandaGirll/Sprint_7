import requests
import allure
import pytest

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES


@allure.feature('Создание курьера')
@allure.story('Позитивный сценарий')
class TestCreateCourierPositive:
    @pytest.mark.positive
    def test_create_courier_success(self, courier_data):

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_courier_success_code"] and
                    response.json() == EXPECTED_RESPONSES["create_courier_success_response"]), \
                f"Ошибка при создании курьера. Код ответа: {response.status_code}, тело ответа: {response.json()}"

    @pytest.mark.positive
    def test_create_courier_without_firstname(self, courier_data):
        with allure.step('Генерация данных курьера без имени'):
            del courier_data['firstName']

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_courier_success_code"] and
                    response.json() == EXPECTED_RESPONSES["create_courier_success_response"]), \
                f"Ошибка при создании курьера без имени. Код ответа: {response.status_code}, тело ответа: {response.json()}"
