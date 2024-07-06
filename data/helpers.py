import json
import requests
from typing import Any, Tuple
from data.data import API_ENDPOINTS
from data.test_data_generator import generate_courier_data, generate_order_data
from itertools import chain, combinations


def extract_response_details(response: Any) -> Tuple[int, str]:
    """
    Извлекает код статуса и сообщение из ответа сервера.

    :param response: Ответ от сервера
    :return: Кортеж с кодом статуса и сообщением
    """
    response_json = response.json()
    response_code = response.status_code
    response_message = response_json.get("message", "")
    return response_code, response_message


def extract_response_ok(response: Any) -> bool:
    """
    Извлекает значение 'ok' из ответа сервера.

    :param response: Ответ от сервера
    :return: Значение 'ok', если оно есть в ответе
    """
    response_json = response.json()
    return response_json.get("ok", False)


def delete_courier(courier_data):
    login_response = requests.post(API_ENDPOINTS["login_courier"], json={
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    courier_id = login_response.json()["id"]
    requests.delete(API_ENDPOINTS["delete_courier"].format(id=courier_id))


class CourierHelper:
    @classmethod
    def setup_class(cls):
        cls.courier_data = generate_courier_data()
        response = requests.post(API_ENDPOINTS["create_courier"], json=cls.courier_data)
        assert response.status_code == 201, "Failed to create test courier. Status code: {response.status_code}, Response: {response.text}"

    @classmethod
    def teardown_class(cls):
        login_response = requests.post(API_ENDPOINTS["login_courier"], json={
            "login": cls.courier_data["login"],
            "password": cls.courier_data["password"]
        })
        courier_id = login_response.json()["id"]
        delete_response = requests.delete(API_ENDPOINTS["delete_courier"].format(id=courier_id))
        assert delete_response.status_code == 200, "Failed to delete test courier. . Status code: {response.status_code}, Response: {response.text}"


class OrderHelper(CourierHelper):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.order_id = None

    @classmethod
    def teardown_class(cls):
        super().teardown_class()
        if cls.order_id:
            cls.delete_order()

    @classmethod
    def delete_order(cls):
        delete_response = requests.put(API_ENDPOINTS["cancel_order"], json={"track": cls.order_id})
        assert delete_response.status_code == 200, f"Failed to delete test order. Status code: {delete_response.status_code}, Response: {delete_response.text}"

    @staticmethod
    def powerset(iterable):
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
