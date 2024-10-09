"""Данные тесты проверяют добавление товара в корзину"""

import pytest
import allure

url = "https://garwin.ru"


@pytest.mark.smoke
@allure.title("Добавление товара из листинга")
def test_add_to_cart_from_listing(page_fixture):
    page_fixture.goto(f'{url}')
    page_fixture.goto("https://garwin.ru/catalog/ruchnoy-instrument")
    # Добавляем первую карточку в листинге
    page_fixture.get_by_text("В корзину").nth(0).click()
    # Проверяем, что счетчик корзины стал равен 1
    badge_text = page_fixture.locator(".Badge__Text").nth(0)
    assert badge_text.inner_text() == "1"
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page_fixture.locator(".ProductTile__Row.ProductTile__Name").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    # Находим первый обьект в классе (первую карточку)(в корзине)
    page_fixture.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(2).click()
    element_cart = page_fixture.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page_fixture.close()

@pytest.mark.smoke
@allure.title("Добавление товара из корзины")
def test_add_to_cart_from_ct(page_fixture):
    # page.goto(f"{url}/tovar/nabor-ruchnyh-instrumentov-94-predmeta", wait_until='domcontentloaded')
    page_fixture.goto("https://garwin.ru/catalog/ruchnoy-instrument")
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page_fixture.locator(".ProductTile__Row.ProductTile__Name").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    page_fixture.locator('.ProductListingOverlayLink').nth(0).click()
    page_fixture.locator('.ProductCardControls__Button').click()
    # Проверяем, что счетчик корзины стал равен 1
    badge_text = page_fixture.locator(".Badge__Text").nth(0)
    assert badge_text.inner_text() == "1"
    page_fixture.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(2).click()
    # Находим первый обьект в классе (первую карточку)(в корзине)
    element_cart = page_fixture.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page_fixture.close()

@allure.title("Добавление товара из поиска")
def test_add_to_cart_from_search(page_fixture):
    page_fixture.goto(f'{url}')
    page_fixture.locator('.kit-input.Field__Input.disable-label').click()
    # Находим первый обьект в классе (первую карточку)(в листинге)
    element_listing = page_fixture.locator(".SearchProductInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_listing = element_listing.inner_text()
    page_fixture.locator('.SearchProductControl__Button.Button.flexRow.size--normal.color--primary').nth(0).click()
    # Проверяем, что счетчик корзины стал равен 1
    badge_text = page_fixture.locator(".Badge__Text").nth(0)
    assert badge_text.inner_text() == "1"
    page_fixture.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(2).click()
    # Находим первый обьект в классе (первую карточку)(в корзине)
    element_cart = page_fixture.locator(".ProductCartInfo__Title").nth(0)
    # Извлекаем текст
    text_ct_cart = element_cart.inner_text()
    # Сравниваем извлеченный текст (наименование) карточки в листинге и карточки в корзине
    assert text_ct_listing == text_ct_cart

    page_fixture.close()


    #Нужно свнять название с первого блока(карточки товара) и сравнить с названием КТ в корзине
