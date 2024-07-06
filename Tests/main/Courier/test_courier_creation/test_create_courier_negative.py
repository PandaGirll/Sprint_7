import pytest
import allure
import requests
from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.test_data_generator import generate_courier_data
from data.helpers import delete_courier


@allure.feature('Создание курьера')
@allure.story('Негативные сценарии')
class TestCreateCourierNegative:

    @pytest.mark.negative
    def test_create_courier_missing_login(self):
        with allure.step('Генерация данных курьера без логина'):
            courier_data = generate_courier_data()
            del courier_data['login']

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["create_courier_missing_data_message"]), \
                f"Ошибка при попытке создания курьера без логина. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_create_courier_missing_password(self):
        with allure.step('Генерация данных курьера без пароля'):
            courier_data = generate_courier_data()
            del courier_data['password']

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["create_courier_missing_data_message"]), \
                f"Ошибка при попытке создания курьера без пароля. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_create_duplicate_courier_failed(self):
        with allure.step('Генерация данных курьера'):
            courier_data = generate_courier_data()

        with allure.step('Создание первого курьера'):
            first_response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)
            assert first_response.status_code == EXPECTED_RESPONSES["create_courier_success_code"], \
                "Не удалось создать первого курьера для теста дубликата"

        with allure.step('Попытка создания дубликата курьера'):
            duplicate_response = requests.post(API_ENDPOINTS["create_courier"], json=courier_data)

        with allure.step('Проверка ответа'):
            assert (duplicate_response.status_code == EXPECTED_RESPONSES["create_courier_duplicate_code"] and
                    duplicate_response.json()["message"] == EXPECTED_RESPONSES["create_courier_duplicate_message"]), \
                f"Ошибка при попытке создания дубликата курьера. Код ответа: {duplicate_response.status_code}, сообщение: {duplicate_response.json()['message']}"

        with allure.step('Удаление созданного курьера'):
            delete_courier(courier_data)