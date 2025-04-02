import time

import allure
import pytest
import pyodbc
import os
import re
import json
import logging
import base64

from dotenv import load_dotenv
from pytest import fail

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.checkout_page import CheckoutPage
from page_objects.header_element import HeaderElement
from page_objects.purchase_page import PurchasePage
from jsonschema import validate, ValidationError


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.custom_schedule
def test_create_order(page_fixture, base_url, delete_recipient_fixture, delete_address_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    purchase_page = PurchasePage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    checkout_page.obtaining_block.create_address(base_url, page_fixture)
    delete_recipient_fixture()
    delete_address_fixture()
    checkout_page.payment_block.click_contact_a_manager_button()
    checkout_page.commentary_block.click_commentary_togle_button()
    checkout_page.commentary_block.fill_commentary_textarea("!!! TEST !!!")
    checkout_page.calculation_block.click_order_button()
    time.sleep(3)
    order_number = purchase_page.memorize_the_order_number()
    print(order_number)
    with allure.step("Проверяю, что номер заказа не пустой"):
        assert order_number != "", "Номер заказа пустой!"
    with allure.step(
            "Проверяю, что номер заказа соответствует одному из шаблонов Х-000000000, ХX000000000, 000000000."):
        pattern = r'^[А-Яа-я-]*\d{9}[А-Яа-я-]*$'

        assert re.match(pattern, order_number), f"Номер заказа '{order_number}' не соответствует шаблону Х-000000000!"


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.for_test_2
@allure.title("Создание заказа с валидацией JSON-схемы")
def test_create_order_schema(page_fixture, base_url, delete_recipient_fixture, delete_address_fixture):
    # try:
    #     # Получаем значение из переменной окружения
    #     json_schema_base64 = os.environ.get("JSON_SCHEMA_BASE64")
    #     if not json_schema_base64:
    #         raise ValueError("JSON_SCHEMA_BASE64 не установлена в переменных окружения")

    #     # Декодируем схему
    #     json_schema_str = base64.b64decode(json_schema_base64).decode('utf-8')
    #     response_schema = json.loads(json_schema_str)
    # except Exception as e:
    #     raise ValueError(f"Ошибка при загрузке JSON схемы: {str(e)}")
        
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    purchase_page = PurchasePage(page_fixture)
    header = HeaderElement(page_fixture)
    cart_page.open(base_url)

    with allure.step("Запоминаю адрес в блоке Получение"):
        company_name = header.company_name_text()

    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)

    name, email, phone = checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    checkout_page.obtaining_block.create_address(base_url, page_fixture)

    delete_recipient_fixture()
    delete_address_fixture()

    with allure.step("Добавляею комментарий к заказу"):
        checkout_page.payment_block.click_contact_a_manager_button()
        checkout_page.commentary_block.click_commentary_togle_button()
        checkout_page.commentary_block.fill_commentary_textarea("!!! TEST !!!")

    with allure.step("Запоминаю адрес в блоке Получение"):
        obtaining_block_adress = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Загружаю JSON-схему"):
        load_dotenv()
        response_schema = json.loads(os.getenv("JSON_SCHEMA"))
    
    # with allure.step("Загружаю JSON-схему"):
    #     load_dotenv()
    #     print(os.environ.keys())
    
        # # Получаем закодированную строку из переменной окружения
        # json_schema_base64 = os.getenv("JSON_SCHEMA_BASE64")
        # if not json_schema_base64:
        #     raise ValueError("JSON_SCHEMA_BASE64 is missing from environment variables")

        # json_schema = os.getenv("JSON_SCHEMA")
        # if not json_schema:
        #     raise ValueError("JSON_SCHEMA is missing from environment variables")
            
        # json_schema_base64 = os.getenv("JSON_SCHEMA_BASE64")
    
        # if json_schema_base64:
        #     # Декодируем Base64
        #     print(f"DEBUG: JSON_SCHEMA_BASE64 = {os.getenv('JSON_SCHEMA_BASE64')[:50]}...")
        #     json_schema_str = base64.b64decode(json_schema_base64).decode("utf-8")
        #     # Загружаем в JSON
        #     response_schema = json.loads(json_schema_str)
        # else:
        #     raise ValueError("JSON_SCHEMA_BASE64 is not set")
    
        with allure.step("Перехватываю запрос и ответ"):
            with (page_fixture.expect_response(os.getenv("METHOD")) as response_info,
                  page_fixture.expect_request(os.getenv("METHOD")) as request_info):
                checkout_page.calculation_block.click_order_button()

    with allure.step("Ожидаю номер заказа"):
        time.sleep(3)
        order_number = purchase_page.memorize_the_order_number()
        print(order_number)

    with allure.step("Проверяю, что номер заказа не пустой"):
        assert order_number != "", "Номер заказа пустой!"

    with allure.step("Проверяю, что номер заказа соответствует шаблону"):
        pattern = r'^[А-Яа-я-]*\d{9}[А-Яа-я-]*$'
        assert re.match(pattern, order_number), f"Номер заказа '{order_number}' не соответствует шаблону!"

    with allure.step("Извлекаю из ответа JSON"):
        response = response_info.value
        response_body = response.json()
        print(json.dumps(response_body, indent=4))

    with allure.step("Проверяю статус код ответа"):
        assert response.status == 200, f"Ожидался статус 200, получен {response.status}"

    with allure.step("Валидирую JSON-схему ответа"):
        try:
            validate(instance=response_body, schema=response_schema)
        except ValidationError as e:
            pytest.fail(f"SCHEMA VALIDATION FAILED:\n"
                        f"Field: {list(e.path)}\n"
                        f"Error: {e.message}\n"
                        f"Value: {e.instance}")

    # Функция для экранирования кавычек
    def escape_json_string(value):
        with allure.step("Экранирует кавычки в строках для корректного JSON"):
            return json.dumps(value)[1:-1]  # убираем внешние кавычки, но экранируем внутри

    with allure.step("Загружаю JSON-схему с проверочными значениями"):
        schema_str = os.getenv("JSON_SCHEMA_TEST")

    with allure.step("Заменяю переменные в схеме на реальные значения с экранированием"):
        schema_str = schema_str.replace("{company_name}", escape_json_string(company_name))
        schema_str = schema_str.replace("{name}", escape_json_string(name))
        schema_str = schema_str.replace("{email}", escape_json_string(email))
        schema_str = schema_str.replace("{phone}", re.sub(r'\D', '', phone))
        with allure.step("Заменяю '{obtaining_block_adress}' на JSON-строку"):
            obtaining_block_adress_json = json.dumps(obtaining_block_adress)  # превращаем объект в строку JSON
            schema_str = schema_str.replace("\"{obtaining_block_adress}\"", obtaining_block_adress_json)

        with allure.step("Преобразую строку обратно в JSON."):
            schema = json.loads(schema_str)

    def to_lower(obj):
        """Рекурсивно приводит все строки в JSON-объекте к нижнему регистру."""
        if isinstance(obj, dict):
            return {k: to_lower(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [to_lower(i) for i in obj]
        elif isinstance(obj, str):
            return obj.lower()
        return obj

    with allure.step("Валидирую JSON-схему ответа"):
        try:
            response_body_lower = to_lower(response_body)
            schema_lower = to_lower(schema)
            validate(instance=response_body_lower, schema=schema_lower)
        except ValidationError as e:
            pytest.fail(f"SCHEMA VALIDATION FAILED:\n"
                        f"Field: {list(e.path)}\n"
                        f"Error: {e.message}\n"
                        f"Value: {e.instance}")

    with allure.step("Проверяю, что комментарий отправился в запросе"):
        request = request_info.value
        try:
            # Получаем тело запроса
            request_body = request.post_data  # Получаем как строку
            if request_body:
                data = json.loads(request_body)
                assert data.get("comment") == "!!! TEST !!!", f"Неверное значение comment: {data.get('comment')}"
        except Exception as e:
            pytest.fail(f"Ошибка при проверке запроса: {e}")





# db_server = os.getenv('DB_SERVER')
# db_name = os.getenv('DB_NAME')
# db_user = os.getenv('DB_USER')
# db_password = os.getenv('DB_PASSWORD')

# Архивный тест с проверкой заказа через SQL
# @pytest.mark.skip("Временно, пока не научимся удалять заказы из аналитики и закрывать в 1С")
# @pytest.mark.smoke
# def create_order(page_fixture, base_url):
#     cart_page = CartPage(page_fixture)
#     autorization = AutorizationModalElement(page_fixture)
#     cart_page.add_to_cart(base_url)
#     cart_page.open(base_url)
#     cart_page.click_order_button()
#     autorization.cart_autorization_send_code_mail_ru()
#     code = autorization.get_autorization_code_mail_ru()
#     autorization.complete_autorization(code)
#     cart_page.click_order_button()
#     #заполняем все поля, выбираем уточнить у менеджера, прописываем комментарий слово "test"
#     time.sleep(2)
#     page_fixture.locator('input[type="text"].kit-input.Field__Input').nth(0).fill("test")
#     page_fixture.locator('input[type="tel"].kit-input.Field__Input').nth(0).fill("+7 (999) 999-99-99")
#     page_fixture.get_by_text("Уточнить у менеджера").nth(0).click()
#     page_fixture.locator(".CheckoutSection__Toggle.Button").click()
#     page_fixture.locator('.kit-textarea.Field__Textarea').fill("!!! TEST !!!")
#     # нажимаем оформить заказ
#     page_fixture.locator(".OrderTotal__Button").click()
#     # Извлекаем номер заказа .PurchaseWithoutPayment__Number извлечь нужно часть текста, после "Номер заказа: "
#     order_number = page_fixture.locator("p.OrderSummary__Number").inner_text().split("Номер заказа: ")[1]
#     print(order_number)
#
#     time.sleep(360)
#
#
#     connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         f'SERVER={db_server};'
#         f'DATABASE={db_name};'
#         f'UID={db_user};'
#         f'PWD={db_password}'
#     )
#
#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT * FROM Buyer_Requests WHERE number = ?"
#             cursor.execute(sql, (order_number,))
#             result = cursor.fetchone()
#
#             assert result is not None, "Order not found in database"
#             print(f"Order {order_number} found in database: {result}")
#     finally:
#         connection.close()
#
#     page_fixture.close()
