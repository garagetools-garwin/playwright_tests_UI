"""Данные тесты проверяют добавление товара в корзину"""

import pytest
import allure

url = "https://garwin.ru"


@pytest.mark.smoke
@allure.title("Добавление товара из листинга")
def test_add_to_cart_from_listing(page):
    page.goto(f'{url}')
    page.goto("https://garwin.ru/catalog/ruchnoy-instrument")
    # Добавляем первую карточку в листинге
    page.get_by_text("В корзину").nth(0).click()
    # Проверяем, что счетчик корзины стал равен 1
    badge_text = page.locator(".Badge__Text").nth(0)
    assert badge_text.inner_text() == "1"
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page.locator(".ProductTile__Row.ProductTile__Name").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    # Находим первый обьект в классе (первую карточку)(в корзине)
    page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(1).click()
    element_cart = page.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page.close()

@pytest.mark.smoke
@allure.title("Добавление товара из корзины")
def test_add_to_cart_from_ct(page):
    # page.goto(f"{url}/tovar/nabor-ruchnyh-instrumentov-94-predmeta", wait_until='domcontentloaded')
    page.goto("https://garwin.ru/catalog/ruchnoy-instrument")
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page.locator(".ProductTile__Row.ProductTile__Name").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    page.locator('.ProductListingOverlayLink').nth(0).click()
    page.locator('.ProductCardControls__Button').click()
    # Проверяем, что счетчик корзины стал равен 1
    badge_text = page.locator(".Badge__Text").nth(0)
    assert badge_text.inner_text() == "1"
    page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(1).click()
    # Находим первый обьект в классе (первую карточку)(в корзине)
    element_cart = page.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page.close()

@allure.title("Добавление товара из поиска")
def test_add_to_cart_from_search(page):
    page.goto(f'{url}')
    page.locator('.kit-input.Field__Input.disable-label').click()
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page.locator(".SearchProductInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    page.locator('.SearchProductControl__Button.Button.flexRow.size--normal.color--primary').nth(0).click()
    # Проверяем, что счетчик корзины стал равен 1
    badge_text = page.locator(".Badge__Text").nth(0)
    assert badge_text.inner_text() == "1"
    page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(1).click()
    # Находим первый обьект в классе (первую карточку)(в корзине)
    element_cart = page.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page.close()


    #Нужно свнять название с первого блока(карточки товара) и сравнить с названием КТ в корзине
