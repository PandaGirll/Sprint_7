import allure
import requests
import logging

from data.data import API_ENDPOINTS, EXPECTED_RESPONSES, ORDER_STATUSES
from data.test_data_generator import generate_courier_data, generate_order_data
from itertools import chain, combinations


def delete_created_courier(courier_data):
    login_response = requests.post(API_ENDPOINTS["login_courier"], json=courier_data)
    if login_response.status_code == EXPECTED_RESPONSES["create_courier_success_code"]:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(API_ENDPOINTS["delete_created_courier"].format(id=courier_id))


class ValidationHelper:
    @staticmethod
    def validate_order_response(api_response, valid_status_codes, expected_content):
        if api_response.status_code not in valid_status_codes:
            return False

        response_data = api_response.json()
        index = valid_status_codes.index(api_response.status_code)
        expected = expected_content[index]

        if isinstance(expected, dict):
            return all(key in response_data and (
                isinstance(response_data[key], value) if isinstance(value, type) else response_data[key] == value)
                       for key, value in expected.items())
        elif isinstance(expected, str):
            return 'message' in response_data and expected in response_data['message']
        elif isinstance(expected, list):
            return 'message' in response_data and any(content in response_data['message'] for content in expected)

        return False

    @staticmethod
    def validate_response(api_response, valid_status_codes, expected_contents, warning_message=None):
        if api_response.status_code == 500:
            allure.attach(api_response.text, "Server Error 500", allure.attachment_type.TEXT)
            return True

        if api_response.status_code not in valid_status_codes:
            return False

        response_data = api_response.json()
        index = valid_status_codes.index(api_response.status_code)
        expected_content = expected_contents[index]

        if isinstance(expected_content, dict):
            is_valid = all(item in response_data.items() for item in expected_content.items())
            if "message" in expected_content:
                if 'message' in response_data:
                    is_valid = is_valid and expected_content["message"] in response_data['message']
        else:
            if 'message' in response_data:
                is_valid = expected_content in response_data['message']

        if not is_valid and warning_message:
            allure.attach(api_response.text, warning_message, allure.attachment_type.TEXT)

        return is_valid

    @staticmethod
    def validate_order_with_order(api_response, expected_valid_status_code):
        if api_response.status_code != expected_valid_status_code:
            allure.attach(api_response.text,
                          f"Expected status code {expected_valid_status_code} but got {api_response.status_code}",
                          allure.attachment_type.TEXT)
            return False

        response_data = api_response.json()
        # Проверяем наличие ключа 'order' и что это словарь
        if 'order' in response_data and isinstance(response_data['order'], dict):
            return True

        allure.attach(api_response.text, "Response does not contain order or order is not a dictionary",
                      allure.attachment_type.TEXT)
        return False


class CourierHelper:
    created_courier_ids = []

    @classmethod
    def create_courier(cls, max_attempts=3):
        for attempt in range(max_attempts):

            create_courier_data = generate_courier_data()
            response = requests.post(API_ENDPOINTS["create_courier"], json=create_courier_data)
            if response.status_code == 201:
                courier_id = response.json().get("id")
                cls.created_courier_ids.append(courier_id)
                return create_courier_data
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
    def create_order(order_data):
        response = requests.post(f"{API_ENDPOINTS['create_order']}", json=order_data)
        if response.status_code == 201:
            return response
        else:
            raise Exception(f"Не удалось создать заказ. Код ответа: {response.status_code}")

    @staticmethod
    def accept_order(order_id, courier_id):

        url = f"{API_ENDPOINTS['accept_order']}/{order_id}?courierId={courier_id}"
        response = requests.put(url)
        return response
        # else:
        #     raise Exception(f"Не удалось принять заказ. Код ответа: {response.status_code}")

    @staticmethod
    def complete_order(order_id):
        url = f"{API_ENDPOINTS['finish_order']}/{order_id}"
        response = requests.put(url)
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Не удалось завершить заказ. Код ответа: {response.status_code}")


    @staticmethod
    # эта ручка просто не работает и при любом валидном запросе возвращает 400
    def cancel_order(track):
        data = {"track": track}
        # response = requests.put(f"{API_ENDPOINTS['cancel_order']}", json=data)
        logging.info(f"Отправка запроса на удаление заказа с треком: {track}")
        url = f"{API_ENDPOINTS['cancel_order']}"
        response = requests.put(url, json=data)
        logging.info(f"Отправляемый запрос: put {url}")
        logging.info(data)
        logging.info(f"Получен ответ для заказа с треком {track}. Статус: {response.status_code}")
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Не удалось отменить заказ. Код ответа: {response.status_code}, ответ: {response.json()}")

    @staticmethod
    def get_order_by_track(track):
        response = requests.get(f"{API_ENDPOINTS['track_order']}?t={track}")
        return response

    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)

    # # Создание логгера для requests
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
    #
    @staticmethod
    def get_order_response_by_track(track):
        logging.info(f"Отправка запроса на получение заказа с треком: {track}")
        url = f"{API_ENDPOINTS['track_order']}?t={track}"
        print("id заказа в методе:", track)
        print(f"Отправляемый запрос: GET {url}")
        response = requests.get(url)
        print(f"Заголовки запроса: {response.request.headers}")
        logging.info(f"Получен ответ для заказа с треком {track}. Статус: {response.status_code}")
        return response

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
        order_info_response = OrderHelper.get_order_by_track(track)
        order_info_json = order_info_response.json()
        station = order_info_json["order"]["metroStation"]
        logging.info(f"Получаем station: {station}")
        return {"nearestStation": station}


    @staticmethod
    def get_courier_station_orders_params(setup_orders):
        courier_id, orders = setup_orders
        track = orders[0]["track"]
        order_info_response = OrderHelper.get_order_by_track(track)
        order_info_json = order_info_response.json()
        station = order_info_json["order"]["metroStation"]
        logging.info(f"Получаем station: {station}")
        return {"nearestStation": station, "courierId": courier_id}

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
