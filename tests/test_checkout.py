"""В этом файле хранятся тесты для чекаут"""
import pytest
import allure

from playwright.sync_api import expect
from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.header_element import HeaderElement



"""Промокод"""

#TODO добавить к тестам test_
@allure.title("Применение валидного промокода")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_aplying_a_valid_promo_code(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    with allure.step("Проверяю, что скидка на плашке равна 5%"):
        assert cart_page.text_discount_budget() == "-5%"
    with allure.step("Проверяю, что цена товара равна его первоначальной стоимости - 5%"):
        assert cart_page.discounted_price() == round(cart_page.base_price() * 0.95, 1)


@allure.title("Применение невалидного промокода")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_aplying_a_invalid_promo_code(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    with allure.step("Запоминую цену товара до активации промокода"):
        pre_action_price = cart_page.order_total_price()
        cart_page.activate_invalid_promo_code()
    with allure.step("Запоминую цену товара после активации промокода"):
        post_action_price = cart_page.order_total_price()
    with allure.step("Проверяю, что цена товара не изменилась"):
        assert pre_action_price == post_action_price
    with allure.step("Проверяю, что плашка со скидкой не отображается"):
        expect(cart_page.discount_budget()).not_to_be_visible()
    with allure.step("Проверяю, что на странице отображается подсказка 'Промокод не действителен'"):
        expect(cart_page.promo_code_field_info()).to_have_text("Промокод не действителен")


@allure.title("Раскрытие блока 'Промокод'")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_promo_code_block(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    with allure.step("Запоминаю положение блока 'Промокод'"):
        promo_code_bar_status = cart_page.promo_code_bar()
    with allure.step("Проверяю, что блок 'Промокод' - раскрыт "):
        expect(promo_code_bar_status).to_have_class('CartPromo__ToggleButton active')
    cart_page.close_promo_code_bar()
    with allure.step("Проверяю, что блок 'Промокод' - закрыт "):
        expect(promo_code_bar_status).not_to_have_class('CartPromo__ToggleButton active')


@allure.title("Применение валидного промокода к неподходящему товару")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_aplying_a_valid_promo_code_on_not_stm_product(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_stm_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    with allure.step("Проверяю, что плашка со скидкой не отображается"):
        expect(cart_page.discount_budget()).not_to_be_visible()
    with allure.step("Проверяю, что на странице отображается подсказка 'В корзине нет товаров, к которым можно применить введенный промокод'"):
        expect(cart_page.promo_code_field_info()).to_have_text("В корзине нет товаров, к которым можно применить введенный промокод")


@allure.title("Отмена промокода")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_canceling_promo_code(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    with allure.step("Запоминую цену товара до активации промокода"):
        pre_action_price = cart_page.order_total_price()
    cart_page.activate_valid_promo_code()
    cart_page.cancel_promo_code()
    with allure.step("Запоминую цену товара после отмены промокода"):
        post_action_price = cart_page.order_total_price()
    with allure.step("Проверяю, что цена до ативации промокода и после его отмены -равны"):
        assert pre_action_price == post_action_price
    with allure.step("Проверяю, что плашка со скидкой не отображается"):
        expect(cart_page.discount_budget()).not_to_be_visible()
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(cart_page.promo_code_field()).to_have_attribute("data-empty", "true")


@allure.title("Очистка поля 'Промокод'")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_cleaning_intput_promo_code(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    cart_page.fill_valid_promo_code()
    cart_page.clear_promo_code_field_by_cross()
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(cart_page.promo_code_field()).to_have_attribute("data-empty", "true")


@allure.title("Активация подсказки")
@pytest.mark.skip("Архив. блок 'Промокод' удалили из корзины")
def checkout_activating_a_hint(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    cart_page.hover_to_promo_code_hint()
    with allure.step("Проверяю, что подсказка отображается на странице"):
        expect(cart_page.promo_code_hint_popup()).to_be_visible()
    with allure.step("Проверяю, что текст подсказки соответствует шаблону"):
        assert cart_page.promo_code_hint_popup_text() == "Промокод действует на отдельные товары и в ограниченный период времени. Подробные условия действия промокода вы можете узнать в описании акции, при получении промокода или у наших специалистов."

# Методы манипулиции с промкодом
# checkout_page.open(base_url)
# checkout_page.price_changes_with_a_promo_code()