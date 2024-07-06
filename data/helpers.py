import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES
from data.test_data_generator import generate_courier_data, generate_order_data
from itertools import chain, combinations


def delete_created_courier(courier_data):
    login_response = requests.post(API_ENDPOINTS["login_courier"], json=courier_data)
    if login_response.status_code == EXPECTED_RESPONSES["create_courier_success_code"]:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id))


class CourierHelper:
    created_courier_ids = []

    @classmethod
    def setup_method(cls, method):
        cls.created_courier_ids = []

    @classmethod
    def teardown_method(cls, method):
        for courier_id in cls.created_courier_ids:
            requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id))

    @classmethod
    def create_courier(cls):
        create_courier_data = generate_courier_data()
        response = requests.post(API_ENDPOINTS["create_courier"], json=create_courier_data)
        if response.status_code == 201:
            courier_id = response.json().get("id")
            cls.created_courier_ids.append(courier_id)
            return create_courier_data
        else:
            raise Exception(f"Не удалось создать тестового курьера. Код ответа: {response.status_code}, Ответ: {response.text}")

    @classmethod
    def login_courier(cls, courier_login, courier_password):
        response = requests.post(API_ENDPOINTS["login_courier"], json={"login": courier_login, "password": courier_password})
        if response.status_code == 200:
            return response.json()["id"]
        else:
            raise Exception(f"Не удалось залогинить курьера. Код ответа: {response.status_code}, Ответ: {response.text}")

    @classmethod
    def delete_courier(cls, courier_id_to_delete):
        response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id_to_delete))
        if response.status_code != 200:
            raise Exception(f"Не удалось удалить тестового курьера. Код ответа: {response.status_code}, Ответ: {response.text}")


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
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    @staticmethod
    def get_orders(**params):
        return requests.get(API_ENDPOINTS["list_orders"], params=params)

    @staticmethod
    def create_order(data=None):
        if data is None:
            data = generate_order_data()
        return requests.post(API_ENDPOINTS["create_order"], json=data)

    @staticmethod
    def create_multiple_orders(count=5):
        orders = []
        for _ in range(count):
            response = OrderHelper.create_order()
            if response.status_code == 201:
                orders.append({"id": response.json()["track"], **response.json()})
        return orders

    @staticmethod
    def accept_order(order_id, courier_id):
        return requests.put(API_ENDPOINTS["accept_order"].format(id=order_id), params={"courierId": courier_id})

    @staticmethod
    def complete_order(order_id, courier_id):
        return requests.put(API_ENDPOINTS["finish_order"].format(id=order_id), json={"id": courier_id})

    @staticmethod
    def cancel_order(track):
        return requests.put(API_ENDPOINTS["cancel_order"], json={"track": track})

    @staticmethod
    def get_order_by_track(track):
        return requests.get(API_ENDPOINTS["track_order"], params={"t": track})

# def extract_response_details(response: Any) -> Tuple[int, str]:
#     """
#     Извлекает код статуса и сообщение из ответа сервера.
#
#     :param response: Ответ от сервера
#     :return: Кортеж с кодом статуса и сообщением
#     """
#     response_json = response.json()
#     response_code = response.status_code
#     response_message = response_json.get("message", "")
#     return response_code, response_message
#
#
# def extract_response_ok(response: Any) -> bool:
#     """
#     Извлекает значение 'ok' из ответа сервера.
#
#     :param response: Ответ от сервера
#     :return: Значение 'ok', если оно есть в ответе
#     """
#     response_json = response.json()
#     return response_json.get("ok", False)
