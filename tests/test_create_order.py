"""Данные тесты проверяют добавление товара в корзину"""
import time
import pytest
import pyodbc
import os

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement

db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

#@pytest.mark.skip("Временно, пока не начимся удалять заказы из аналитики и закрывать в 1С")
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
    page_fixture.locator(".CheckoutSection__Toggle.Button").click()
    page_fixture.locator('.kit-textarea.Field__Textarea').fill("!!! TEST !!!")
    # нажимаем оформить заказ
    page_fixture.locator(".OrderTotal__Button").click()
    # Извлекаем номер заказа .PurchaseWithoutPayment__Number извлечь нужно часть текста, после "Номер заказа: "
    order_number = page_fixture.locator("p.OrderSummary__Number").inner_text().split("Номер заказа: ")[1]
    print(order_number)

    time.sleep(360)

***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***

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
