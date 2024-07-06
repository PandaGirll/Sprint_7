import sys
import os
import pytest
from data.helpers import OrderHelper, CourierHelper, delete_created_courier
from data.test_data_generator import generate_courier_data

# Добавляем корневую директорию проекта в PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# @pytest.fixture(scope="function")
# def setup_orders():
#     # Создаем курьера
#     courier = CourierHelper.create_courier()
#
#     # Создаем несколько заказов
#     orders = OrderHelper.create_multiple_orders(5)
#
#     # Принимаем первые три заказа курьером
#     for order in orders[:3]:
#         OrderHelper.accept_order(order['id'], courier['id'])
#
#     # Завершаем первые два заказа
#     for order in orders[:2]:
#         OrderHelper.complete_order(order['id'], courier['id'])
#
#     yield courier, orders
#
#     # Очистка: отменяем все заказы и удаляем курьера
#     for order in orders:
#         OrderHelper.cancel_order(order['id'])
#     CourierHelper.delete_courier(courier['id'])


@pytest.fixture
def courier_data():
    data = generate_courier_data()  # Используем напрямую функцию генерации данных
    yield data
    try:
        delete_created_courier(data)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")

@pytest.fixture
def setup_and_teardown_courier():
    # Setup
    setup_courier_data = CourierHelper.create_courier()
    yield setup_courier_data
    # Teardown
    try:
        courier_id = CourierHelper.login_courier(setup_courier_data["login"], setup_courier_data["password"])
        CourierHelper.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")
