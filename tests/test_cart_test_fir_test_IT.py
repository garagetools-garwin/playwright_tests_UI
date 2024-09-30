"""в этом файле я тестирую уменьшение количество фикстур в set up"""
import time
import pytest
import allure
from playwright.sync_api import expect
import testit

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.header_element import HeaderElement



@pytest.mark.testit_case_title("Активация блока изменения информации_testIT1")
@testit.title("Активация блока изменения информации_testIT2")
@allure.title("Активация блока изменения информации")
def cart_info_change_block_activation(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    expect(cart_page.change_info_block).to_be_visible()

@pytest.mark.testit_case_title("Открытие модального окна авторизации_testIT1")
@testit.title("Открытие модального окна авторизации_testIT2")
@allure.title("Открытие модального окна авторизации")
def test_cart_autorization_modal(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    autorization = AutorizationModalElement(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_order_button()
    with allure.step("Проверяю, что окно аторизаци отображается на странице"):
        expect(autorization.autorization_modal).to_be_visible()












