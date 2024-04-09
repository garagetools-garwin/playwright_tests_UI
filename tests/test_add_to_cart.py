"""Этот тест проверяет добавление товара в корзину"""

import pytest

url = "https://garwin.ru"


@pytest.mark.smoke
def test_autorization(page):
    page.goto(f'{url}')
    page.goto("https://garwin.ru/catalog/ruchnoy-instrument")
    page.get_by_text("В корзину").nth(0).click()
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page.locator(".ProductTile__Row.ProductTile__Name").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    print("Извлеченный текст:", text_ct_listing)
    # Находим первый обьект в классе (первую карточку)(в корзине)
    page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(1).click()
    element_cart = page.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    print("Извлеченный текст:", text_ct_cart)
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page.close()


    #Нужно свнять название с первого блока(карточки товара) и сравнить с названием КТ в корзине
