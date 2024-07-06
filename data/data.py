# data.py

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/"

# Ручки API
API_ENDPOINTS = {
    "create_courier": f"{BASE_URL}/courier",
    "login_courier": f"{BASE_URL}/courier/login",
    "delete_courier": f"{BASE_URL}/courier/{{id}}",
    "list_orders": f"{BASE_URL}/orders",
    "create_order": f"{BASE_URL}/orders",
    "accept_order": f"{BASE_URL}/orders/accept/{{id}}",
    "track_order": f"{BASE_URL}/orders/track",
}

# Ожидаемые тексты ответов от API
EXPECTED_RESPONSES = {
    "create_courier_success_code": 201,
    "create_courier_success_response": {"ok": True},
    "create_courier_missing_data_code": 400,
    "create_courier_missing_data_message": "Недостаточно данных для создания учетной записи",
    "create_courier_duplicate_code": 409,
    "create_courier_duplicate_message": "Этот логин уже используется. Попробуйте другой.",

    "login_courier_success_code": 200,
    "login_courier_success_response": {"id": 12345},
    "login_courier_missing_data_code": 400,
    "login_courier_missing_data_message": "Недостаточно данных для входа",
    "login_courier_invalid_code": 404,
    "login_courier_invalid_message": "Учетная запись не найдена",
    "login_courier_missing_field_code": 504,
    "login_courier_missing_field_message": "Service unavailable",

    "delete_courier_success_code": 200,
    "delete_courier_success_response": {"ok": True},
    "delete_courier_missing_data_code": 400,
    "delete_courier_missing_data_message": "Недостаточно данных для удаления курьера",
    "delete_courier_not_found_code": 404,
    "delete_courier_not_found_message": "Курьера с таким id нет",

    "get_courier_orders_count_success_code": 200,
    "get_courier_orders_count_success_response": {"id": "123456", "ordersCount": "100500"},
    "get_courier_orders_count_missing_data_code": 400,
    "get_courier_orders_count_missing_data_message": "Недостаточно данных для поиска",
    "get_courier_orders_count_not_found_code": 404,
    "get_courier_orders_count_not_found_message": "Курьер не найден",

    "finish_order_success_code": 200,
    "finish_order_success_response": {"ok": True},
    "finish_order_missing_data_code": 400,
    "finish_order_missing_data_message": "Недостаточно данных для поиска",
    "finish_order_not_found_order_code": 404,
    "finish_order_not_found_order_message": "Заказа с таким id не существует",
    "finish_order_not_found_courier_code": 404,
    "finish_order_not_found_courier_message": "Курьера с таким id не существует",
    "finish_order_conflict_code": 409,
    "finish_order_conflict_message": "Этот заказ нельзя завершить",

    "cancel_order_success_code": 200,
    "cancel_order_success_response": {"ok": True},
    "cancel_order_missing_data_code": 400,
    "cancel_order_missing_data_message": "Недостаточно данных для поиска",
    "cancel_order_not_found_code": 404,
    "cancel_order_not_found_message": "Заказ не найден",
    "cancel_order_conflict_code": 409,
    "cancel_order_conflict_message": "Этот заказ уже в работе",

    "get_orders_list_success_code": 200,
    "get_orders_list_success_response": {
        "orders": [
            {"id": 5, "courierId": None, "firstName": "вфцфвц", "lastName": "вфцвфцв", "address": "вфцвфцвфц",
             "metroStation": "4", "phone": "1441412414", "rentTime": 4, "deliveryDate": "2020-06-08T21:00:00.000Z",
             "track": 189237, "color": "", "comment": "вфцвфцвфцв", "createdAt": "2020-06-21T13:23:09.404Z",
             "updatedAt": "2020-06-21T13:23:09.404Z", "status": 0}
        ],
        "pageInfo": {"page": 0, "total": 3, "limit": 2},
        "availableStations": ""
    },
    "get_orders_list_courier_not_found_code": 404,
    "get_orders_list_courier_not_found_message": "Курьер с идентификатором {courierId} не найден",

    "get_order_by_track_success_code": 200,
    "get_order_by_track_success_response": {
        "order": {
            "id": 2,
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Kanoha, 142 apt.",
            "metroStation": "1",
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06T00:00:00.000Z",
            "track": 521394,
            "status": 1,
            "color": "",
            "comment": "Saske, come back to Kanoha",
            "cancelled": False,
            "finished": False,
            "inDelivery": False,
            "courierFirstName": "Kaneki",
            "createdAt": "2020-06-08T14:40:28.219Z",
            "updatedAt": "2020-06-08T14:40:28.219Z"
        }
    },
    "get_order_by_track_missing_data_code": 400,
    "get_order_by_track_missing_data_message": "Недостаточно данных для поиска",
    "get_order_by_track_not_found_code": 404,
    "get_order_by_track_not_found_message": "Заказ не найден",

    "accept_order_success_code": 200,
    "accept_order_success_response": {"ok": True},
    "accept_order_missing_data_code": 400,
    "accept_order_missing_data_message": "Недостаточно данных для поиска",
    "accept_order_not_found_order_code": 404,
    "accept_order_not_found_order_message": "Заказа с таким id не существует",
    "accept_order_not_found_courier_code": 404,
    "accept_order_not_found_courier_message": "Курьера с таким id не существует",
    "accept_order_conflict_code": 409,
    "accept_order_conflict_message": "Этот заказ уже в работе",
    "accept_order_conflict_missing_data_code": 400,
    "accept_order_conflict_missing_data_message": "Недостаточно данных для поиска",

    "create_order_success_code": 201,
    "create_order_success_response": {"track": 124124},
    "create_order_missing_field_code": 400,
    "create_order_missing_field_message": "Не заполнено обязательное поле {field}",
    "create_order_empty_field_code": 400,
    "create_order_empty_field_message": "Поле {field} не может быть пустым",

    "ping_server_success_code": 200,
    "ping_server_success_message": "pong",

    "search_stations_success_code": 200,
    "search_stations_success_message": "OK"
}

ORDER_COLORS = ["BLACK", "GREY"]

