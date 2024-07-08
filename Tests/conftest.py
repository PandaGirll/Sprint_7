import os
import sys
import time
import logging
import pytest

from data.helpers import OrderHelper, CourierHelper, delete_created_courier
from data.test_data_generator import generate_courier_data, generate_order_data

# Добавляем корневую директорию проекта в PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def courier_data():
    data = generate_courier_data()
    yield data
    try:
        delete_created_courier(data)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")


@pytest.fixture
def setup_and_teardown_courier():
    # Setup
    create_courier_data = CourierHelper.create_courier()
    yield create_courier_data
    # Teardown
    try:
        courier_id = CourierHelper.login_courier(create_courier_data["login"], create_courier_data["password"])
        CourierHelper.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")


@pytest.fixture
def setup_and_teardown_order_with_track():
    order_helper = OrderHelper()
    order_data = generate_order_data()
    response = order_helper.create_order(order_data)
    order_track = response.json()['track']
    logging.info(f"Создан заказ с треком: {order_track}")

    yield order_track


# из-за бага api заказ невозможно отменить
# if order_track:
#     order_helper.cancel_order(order_track)
#     logging.info(f"Заказ с треком {order_track} успешно отменен")



@pytest.fixture(scope="function")
def setup_orders_for_list_tests():
    # Setup
    courier_helper = CourierHelper()
    order_helper = OrderHelper()
    # Создание курьера
    new_courier = courier_helper.create_courier()
    assert new_courier, "Ошибка при создании курьера."
    print(f"Курьер создан: {new_courier}")
    # Логин курьера для получения id
    courier_id = courier_helper.login_courier(new_courier["login"], new_courier["password"])
    assert courier_id, "Ошибка при логине курьера."
    print(f"Курьер вошел в систему с ID: {courier_id}")
    # Создание 5 заказов
    orders = []
    for _ in range(5):
        order_data = generate_order_data()
        response = order_helper.create_order(order_data)
        assert response.status_code == 201, f"Не удалось создать заказ: {response.json()}"
        track = response.json()['track']
        print(f"Создан заказ с треком: {track}")
        # Нужна задержка, иначе api не успевает обработать все заказы
        time.sleep(5)
        # Получение информации о заказе по его номеру (track)
        order_details = order_helper.get_order_by_track(track)
        assert order_details.status_code == 200, f"Не удалось получить детали заказа: {order_details.json()}"
        order_id = order_details.json()["order"]["id"]
        print(f"Получены детали заказа. ID заказа: {order_id}")
        orders.append({"track": track, "id": order_id})

    assert len(orders) == 5, "Не все заказы были успешно созданы."
    # Принятие курьером 3 заказов
    for order in orders[:3]:
        response = order_helper.accept_order(order['id'], courier_id)
        assert response.status_code == 200, f"Не удалось принять заказ {order['id']} курьером {courier_id}: {response.status_code}, {response.json()}"
        print(f"Заказ {order['id']} принят курьером {courier_id}")
    # Завершение 2 заказов
    for order in orders[:2]:
        response = order_helper.complete_order(order['id'])
        assert response.status_code == 200, f"Не удалось завершить заказ {order['id']} курьером {courier_id}: {response.status_code}, {response.json()}"
        print(f"Заказ {order['id']} завершен курьером {courier_id}")
    yield courier_id, orders
    # Teardown
    courier_helper.delete_courier(courier_id)


@pytest.fixture
def courier_for_deletion():
    # Setup
    courier_for_del = CourierHelper.create_courier()
    courier_id = CourierHelper.login_courier(courier_for_del["login"], courier_for_del["password"])
    yield courier_id
    # Teardown не нужен, так как курьер будет удален в рамках теста


@pytest.fixture
def order_and_courier_setup():
    courier_helper = CourierHelper()
    order_helper = OrderHelper()
    # Создаем курьера
    test_courier_data = courier_helper.create_courier()
    courier_id = courier_helper.login_courier(test_courier_data["login"], test_courier_data["password"])
    # Создаем заказ
    order_info = generate_order_data()
    order_response = order_helper.create_order(order_info)
    order_track = order_response.json()['track']
    # Добавляем задержку в 5 секунд, иначе из-за плохого интернета часть тестов падает
    time.sleep(5)
    order_data = order_helper.get_order_by_track(order_track)
    order_id = order_data.json()["order"]["id"]
    time.sleep(3)
    yield order_id, courier_id
    time.sleep(3)
    # Очистка после теста
    courier_helper.delete_courier(courier_id)
    # order_helper.cancel_order(order_id)
