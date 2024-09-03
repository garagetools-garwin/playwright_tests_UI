"""Данные тесты проверяют добавление товара в корзину"""
import time
import pytest
import pyodbc

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement

@pytest.mark.skip("Временно")
@pytest.mark.smoke
def test_add_to_cart_from_listing(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    autorization = AutorizationModalElement(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_order_button()
    autorization.cart_autorization_send_code()
    code = autorization.get_autorization_code_mail_ru()
    autorization.complete_autorization(code)
    cart_page.click_order_button()
    #заполняем все поля, выбираем уточнить у менеджера, прописываем комментарий слово "test"
    time.sleep(2)
    page_fixture.locator('input[type="text"].kit-input.Field__Input').nth(0).fill("test")
    page_fixture.locator('input[type="tel"].kit-input.Field__Input').nth(0).fill("+7 (999) 999-99-99")
    page_fixture.get_by_text("Уточнить у менеджера").nth(0).click()
    page_fixture.locator('.kit-textarea.Field__Textarea').fill("!!! TEST !!!")
    # нажимаем оформить заказ
    page_fixture.get_by_text("Оформить заказ").nth(0).click()
    # Извлекаем номер заказа .PurchaseWithoutPayment__Number извлечь нужно часть текста, после "Номер заказа: "
    order_number = page_fixture.locator(".PurchaseWithoutPayment__Number").inner_text().split("Номер заказа: ")[1]
    print(order_number)

    time.sleep(360)

    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=1cdwh;'
        'DATABASE=dwhsample;'
        'UID=dwh;'
        'PWD=dwhsample'
    )

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Buyer_Requests WHERE number = ?"
            cursor.execute(sql, (order_number,))
            result = cursor.fetchone()

            assert result is not None, "Order not found in database"
            print(f"Order {order_number} found in database: {result}")
    finally:
        connection.close()

    page_fixture.close()



# @pytest.mark.smoke
# def test_add_to_cart_from_listing(page_fixture, base_url):
#     cart_page = CartPage(page_fixture)
#     urls_to_check = [
#         "https://garwin.ru/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd",
#         "https://garwin.ru/tovar/bita-udarnaya-1-4-ph1-25mm"
#     ]
#
#     for url in urls_to_check:
#         page.goto(url)
#
#         try:
#             # Попытка найти и нажать кнопку "Добавить в корзину"
#             page.get_by_text(" Добавить в корзину ").click()
#             break  # Прерываем цикл, если кнопка найдена и товар добавлен
#         except Exception:
#             print(f"Add to cart button not found on {url}")
#             continue  # Переходим к следующей ссылке, если кнопка не найдена
#     else:
#         raise ValueError("Product not available, please select another product")
#
#     page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(2).click()
#     #нажимаем на оформить заказ
#     page.get_by_text("Оформить заказ").click()
#     #заполняем все поля, выбираем уточнить у менеджера, прописываем комментарий слово "test"
#     time.sleep(2)
#     page.locator('input[type="text"].kit-input.Field__Input').nth(0).fill("test")
#     page.locator('input[type="tel"].kit-input.Field__Input').nth(0).fill("+7 (999) 999-99-99")
#     page.get_by_text("Уточнить у менеджера").nth(0).click()
#     page.locator('.kit-textarea.Field__Textarea').fill("!!! TEST !!!")
#     # нажимаем оформить заказ
#     page.get_by_text("Оформить заказ").nth(0).click()
#     # Извлекаем номер заказа .PurchaseWithoutPayment__Number извлечь нужно часть текста, после "Номер заказа: "
#     order_number = page.locator(".PurchaseWithoutPayment__Number").inner_text().split("Номер заказа: ")[1]
#     print(order_number)
#
#     time.sleep(360)
#
#     connection = pyodbc.connect(
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'SERVER=1cdwh;'
#         'DATABASE=dwhsample;'
#         'UID=dwh;'
#         'PWD=dwhsample'
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
#     page.close()
