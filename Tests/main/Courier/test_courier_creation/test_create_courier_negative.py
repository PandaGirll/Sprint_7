import allure
import pytest
import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES


@allure.feature('Создание курьера')
@allure.story('Негативные сценарии')
class TestCreateCourierNegative:

    @pytest.mark.negative
    def test_create_courier_missing_login(self, courier_data):
        with allure.step('Генерация данных курьера без логина'):
            del courier_data['login']

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["create_courier_missing_data_message"]), \
                f"Ошибка при попытке создания курьера без логина. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_create_courier_missing_password(self, courier_data):
        with allure.step('Генерация данных курьера без пароля'):
            del courier_data['password']

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["create_courier_missing_data_message"]), \
                f"Ошибка при попытке создания курьера без пароля. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_create_duplicate_courier_failed(self, courier_data):
        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)
            assert response.status_code == EXPECTED_RESPONSES[
                "create_courier_success_code"], "Не удалось создать первого курьера"

        with allure.step('Попытка создания дубликата курьера'):
            duplicate_response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (duplicate_response.status_code == EXPECTED_RESPONSES["create_courier_duplicate_code"] and
                    duplicate_response.json()["message"] == EXPECTED_RESPONSES["create_courier_duplicate_message"]), \
                f"Ошибка при попытке создания дубликата курьера. Код ответа: {duplicate_response.status_code}, сообщение: {duplicate_response.json()['message']}"
