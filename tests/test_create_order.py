"""Данные тесты проверяют добавление товара в корзину"""
import time

import allure
import pytest
import pyodbc
import os
import re

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.checkout_page import CheckoutPage
from page_objects.purchase_page import PurchasePage

db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')


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
    checkout_page.payment_block.click_check_with_manager_button()
    checkout_page.commentary_block.click_commentary_togle_button()
    checkout_page.commentary_block.fill_commentary_textarea("!!! TEST !!!")
    checkout_page.calculation_block.click_order_button()
    order_number = purchase_page.memorize_the_order_number()
    print(order_number)
    with allure.step("Проверяю, что номер заказа не пустой"):
        assert order_number != "", "Номер заказа пустой!"
    with allure.step("Проверяю, что номер заказа соответствует одному из шаблонов Х-000000000, ХX000000000, 000000000."):
        pattern = r'^[А-Яа-я-]*\d{9}[А-Яа-я-]*$'
        assert re.match(pattern, order_number), f"Номер заказа '{order_number}' не соответствует шаблону Х-000000000!"

    # TODO: настроить отдельное расписание для этого теста
    # TODO: вставить фикстуру удаления в метод создания получателя и адреса


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
