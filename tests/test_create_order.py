"""Данные тесты проверяют добавление товара в корзину"""
import time
import pytest
import pyodbc

url = "https://garwin.ru"


@pytest.mark.smoke
def test_add_to_cart_from_listing(page):
    urls_to_check = [
        "https://garwin.ru/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd",
        "https://garwin.ru/tovar/bita-udarnaya-1-4-ph1-25mm"
    ]

    for url in urls_to_check:
        page.goto(url)

        try:
            # Попытка найти и нажать кнопку "Добавить в корзину"
            page.get_by_text(" Добавить в корзину ").click()
            break  # Прерываем цикл, если кнопка найдена и товар добавлен
        except Exception:
            print(f"Add to cart button not found on {url}")
            continue  # Переходим к следующей ссылке, если кнопка не найдена
    else:
        raise ValueError("Product not available, please select another product")

    page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(1).click()
    #нажимаем на оформить заказ
    page.get_by_text("Оформить заказ").click()
    #заполняем все поля, выбираем уточнить у менеджера, прописываем комментарий слово "test"
    time.sleep(2)
    page.locator('input[type="text"].kit-input.Field__Input').nth(0).fill("test")
    page.locator('input[type="tel"].kit-input.Field__Input').nth(0).fill("+7 (999) 999-99-99")
    page.get_by_text("Уточнить у менеджера").nth(0).click()
    page.locator('.kit-textarea.Field__Textarea').fill("!!! TEST !!!")
    # нажимаем оформить заказ
    page.get_by_text("Оформить заказ").nth(0).click()
    # Извлекаем номер заказа .PurchaseWithoutPayment__Number извлечь нужно часть текста, после "Номер заказа: "
    order_number = page.locator(".PurchaseWithoutPayment__Number").inner_text().split("Номер заказа: ")[1]
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

    page.close()
