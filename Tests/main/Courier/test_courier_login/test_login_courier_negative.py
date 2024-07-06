import pytest
import allure
import requests
from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.helpers import CourierHelper


@allure.feature('Логин курьера')
@allure.story('Негативные сценарии')
class TestLoginCourierNegative:

    @pytest.mark.negative
    def test_courier_login_missing_login_field(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        with allure.step('Отправка запроса на логин без поля login'):
            response = requests.post(API_ENDPOINTS["login_courier"], json={
                "password": courier["password"]
            })

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["login_courier_missing_data_message"]), \
                f"Ошибка при попытке входа без поля login. Код ответа: {response.status_code}, сообщение: {response.text}"

    @pytest.mark.negative
    def test_courier_login_empty_login(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        with allure.step('Отправка запроса на логин с пустым login'):
            response = requests.post(API_ENDPOINTS["login_courier"], json={
                "login": "",
                "password": courier["password"]
            })

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["login_courier_missing_data_message"]), \
                f"Ошибка при попытке входа с пустым login. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_courier_login_missing_password_field(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        with allure.step('Отправка запроса на логин без поля password'):
            response = requests.post(API_ENDPOINTS["login_courier"], json={
                "login": courier["login"]
            })

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_missing_field_code"] and
                    response.text == EXPECTED_RESPONSES["login_courier_missing_field_message"]), \
                f"Ошибка при попытке входа без поля password. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_courier_login_empty_password(self, setup_and_teardown_courier):
        courier = setup_and_teardown_courier
        with allure.step('Отправка запроса на логин с пустым password'):
            response = requests.post(API_ENDPOINTS["login_courier"], json={
                "login": courier["login"],
                "password": ""
            })

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_missing_data_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["login_courier_missing_data_message"]), \
                f"Ошибка при попытке входа с пустым password. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

    @pytest.mark.negative
    def test_courier_login_nonexistent_credentials(self):
        with allure.step('Отправка запроса на логин с несуществующими учетными данными'):
            response = requests.post(API_ENDPOINTS["login_courier"], json={
                "login": "nonexistent_user",
                "password": "nonexistent_password"
            })

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["login_courier_invalid_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["login_courier_invalid_message"]), \
                f"Ошибка при попытке входа с несуществующими учетными данными. Код ответа: {response.status_code}, сообщение: {response.json()['message']}"

