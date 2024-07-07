import requests

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES, ORDER_STATUSES
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
    def create_courier(cls, max_attempts=3):
        for attempt in range(max_attempts):

            create_courier_data = generate_courier_data()
            response = requests.post(API_ENDPOINTS["create_courier"], json=create_courier_data)
            if response.status_code == 201:
                courier_id = response.json().get("id")
                cls.created_courier_ids.append(courier_id)
                return response, create_courier_data
        raise Exception(
            f"Не удалось создать тестового курьера после {max_attempts} попыток. Код ответа: {response.status_code}, Ответ: {response.text}")

    @classmethod
    def login_courier(cls, courier_login, courier_password):
        response = requests.post(API_ENDPOINTS["login_courier"],
                                 json={"login": courier_login, "password": courier_password})
        if response.status_code == 200:
            return response.json()["id"]
        else:
            raise Exception(
                f"Не удалось залогинить курьера. Код ответа: {response.status_code}, Ответ: {response.text}")

    @classmethod
    def delete_courier(cls, courier_id_to_delete):
        response = requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id_to_delete))
        if response.status_code != 200:
            raise Exception(
                f"Не удалось удалить тестового курьера. Код ответа: {response.status_code}, Ответ: {response.text}")


class OrderHelper:
    def __init__(self):
        self.order_id = None

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
        response = requests.post(API_ENDPOINTS["create_order"], json=data)
        return response

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
        response = requests.get(f"{API_ENDPOINTS['track_order']}?t={track}")
        if response.status_code == 200:
            order_data = response.json().get('order')
            if order_data:
                return order_data
            else:
                raise ValueError("Данные о заказе отсутствуют в ответе API")
        else:
            raise Exception(f"Не удалось получить информацию о заказе. Код ответа: {response.status_code}")

    @staticmethod
    def generate_order_without_field(field):
        order_data = generate_order_data()
        del order_data[field]
        return order_data

    @staticmethod
    def generate_order_with_empty_field(field):
        order_data = generate_order_data()
        order_data[field] = ""
        return order_data


class OrderParamsHelper:
    @staticmethod
    def get_courier_orders_params(setup_orders, status):
        courier_id, _ = setup_orders
        params = {"courierId": courier_id}
        if status == "completed":
            params["status"] = ORDER_STATUSES["COMPLETED"]
        return params

    @staticmethod
    def get_station_orders_params(setup_orders):
        courier_id, orders = setup_orders
        track = orders[0]["track"]
        order_info = OrderHelper.get_order_by_track(track)
        station = order_info["metroStation"]
        return {"nearestStation": f"[{station}]", "courierId": courier_id}

    @staticmethod
    def get_courier_station_orders_params(setup_orders):
        courier_id, orders = setup_orders
        track = orders[0]["track"]
        order_info = OrderHelper.get_order_by_track(track)
        station = order_info["metroStation"]
        return {"nearestStation": f"[{station}]", "courierId": courier_id}

    @staticmethod
    def check_response(response, expected_code, expected_response):
        if response.status_code != expected_code:
            return False

        json_response = response.json()

        for key, expected_type in expected_response.items():
            if key not in json_response:
                return False
            if not isinstance(json_response[key], expected_type):
                return False

        return True

    @staticmethod
    def get_limit_page_orders_params():
        return {"limit": 10, "page": 1}
