import pytest
import allure
import requests
from data.data import API_ENDPOINTS, EXPECTED_RESPONSES, ORDER_COLORS
from data.test_data_generator import generate_order_data
from data.helpers import OrderHelper


@allure.feature('Создание заказа')
@allure.story('Позитивные сценарии')
class TestCreateOrderPositive(OrderHelper):

    @pytest.mark.positive
    @pytest.mark.parametrize("color", list(OrderHelper.powerset(ORDER_COLORS)))
    @allure.title("Создание заказа с цветом: {color}")
    def test_create_order(self, color):
        with allure.step(f'Генерация данных заказа с цветом {color}'):
            order_data = generate_order_data()
            order_data['color'] = list(color) if color else None

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(API_ENDPOINTS["create_order"], json=order_data)

        with allure.step('Проверка ответа'):
            assert (response.status_code == EXPECTED_RESPONSES["create_order_success_code"] and
                    "track" in response.json()), \
                f"Ошибка при создании заказа. Код ответа: {response.status_code}, ответ: {response.json()}"

        self.order_id = response.json()["track"]
