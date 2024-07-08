import pytest
import allure
import requests
from data.data import API_ENDPOINTS, EXPECTED_RESPONSES


@allure.feature('Удаление курьера')
@allure.story('Негативные сценарии')
class TestDeleteCourierNegative:

    @pytest.mark.negative
    @allure.title("Удаление курьера без указания id")
    def test_delete_courier_without_id(self):
        with allure.step('Отправка запроса на удаление курьера без id'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=""))

        with allure.step('Проверка ответа'):
            assert ((response.status_code == EXPECTED_RESPONSES["delete_courier_missing_data_code"] and
                     response.json()["message"] == EXPECTED_RESPONSES["delete_courier_missing_data_message"]) or
                    (response.status_code == EXPECTED_RESPONSES["delete_courier_not_found_code"])), \
                f"Неожиданный ответ при удалении курьера без id. Получено: код {response.status_code} и сообщение {response.json()['message']}"

        if (response.status_code != EXPECTED_RESPONSES["delete_courier_missing_data_code"] or
                response.json()["message"] != EXPECTED_RESPONSES["delete_courier_missing_data_message"]):
            allure.attach(
                "Предупреждение",
                f"Ответ сервера не соответствует ожидаемому. " +
                f"Ожидалось: код {EXPECTED_RESPONSES['delete_courier_missing_data_code']}, " +
                f"сообщение '{EXPECTED_RESPONSES['delete_courier_missing_data_message']}'. " +
                f"Получено: код {response.status_code}, сообщение '{response.json()['message']}'.",
                allure.attachment_type.TEXT
            )

    @pytest.mark.negative
    @allure.title("Удаление несуществующего курьера")
    def test_delete_nonexistent_courier(self):
        nonexistent_id = 999999

        with allure.step(f'Отправка запроса на удаление несуществующего курьера с id {nonexistent_id}'):
            response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=nonexistent_id))

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["delete_courier_not_found_code"] and
                    response.json()["message"] == EXPECTED_RESPONSES["delete_courier_not_found_message"]), \
                f"Неожиданный ответ при удалении несуществующего курьера. Получено: код {response.status_code} и сообщение {response.json()['message']}"

        if (response.status_code != EXPECTED_RESPONSES["delete_courier_not_found_code"] or
                response.json()["message"] != EXPECTED_RESPONSES["delete_courier_not_found_message"]):
            allure.attach(
                "Предупреждение",
                f"Ответ сервера не соответствует ожидаемому. " +
                f"Ожидалось: код {EXPECTED_RESPONSES['delete_courier_not_found_code']}, " +
                f"сообщение '{EXPECTED_RESPONSES['delete_courier_not_found_message']}'. " +
                f"Получено: код {response.status_code}, сообщение '{response.json()['message']}'.",
                allure.attachment_type.TEXT
            )
