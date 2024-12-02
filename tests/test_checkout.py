"""В этом файле хранятся тесты для чекаут"""
import pytest
import allure

from playwright.sync_api import expect
from page_objects.checkout_page import CheckoutPage
from page_objects.cart_page import CartPage


from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.header_element import HeaderElement


"""Промокод"""


#TODO добавить к тестам test_
#TODO перевести методы связаные с блоком калькуляции в checkout_page

@pytest.mark.auth
@allure.title("Применение валидного промокода")
def test_checkout_aplying_a_valid_promo_code(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.check_promo_code()
    with allure.step("Запоминю цену товара до активации промокода"):
        base_price = checkout_page.base_price()
        checkout_page.activate_valid_promo_code()
    with allure.step("Запоминаю цену товара после активации промокода"):
        discounted_price = checkout_page.base_price()
    with allure.step("Проверяю, что цена товара равна его первоначальной стоимости - 5%"):
        assert discounted_price == round(base_price * 0.95, 2)


@pytest.mark.auth
@allure.title("Применение невалидного промокода")
def test_checkout_aplying_a_invalid_promo_code(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.check_promo_code()
    with allure.step("Запоминю цену товара до активации промокода"):
        pre_action_price = checkout_page.base_price()
        checkout_page.activate_invalid_promo_code()
    with allure.step("Запоминаю цену товара после активации промокода"):
        post_action_price = checkout_page.base_price()
    with allure.step("Проверяю, что цена товара не изменилась"):
        assert pre_action_price == post_action_price
    with allure.step("Проверяю, что на странице отображается подсказка 'Промокод не действителен'"):
        expect(checkout_page.promo_code_field_info()).to_have_text("Промокод не действителен")


@pytest.mark.auth
@allure.title("Раскрытие блока 'Промокод'")
def test_checkout_promo_code_block(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.open_promo_code_bar()
    with allure.step("Запоминаю положение блока 'Промокод'"):
        promo_code_bar_status = checkout_page.promo_code_bar()
    with allure.step("Проверяю, что блок 'Промокод' - раскрыт "):
        expect(promo_code_bar_status).to_have_class('PromoWidget__ToggleButton --is-active')
    checkout_page.close_promo_code_bar()
    with allure.step("Проверяю, что блок 'Промокод' - закрыт "):
        expect(promo_code_bar_status).not_to_have_class('PromoWidget__ToggleButton --is-active')


@pytest.mark.auth
@allure.title("Применение валидного промокода к неподходящему товару")
def test_checkout_aplying_a_valid_promo_code_on_not_stm_product(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_stm_product(base_url)
    checkout_page.open(base_url)
    checkout_page.check_promo_code()
    checkout_page.activate_valid_promo_code()
    with allure.step("Проверяю, что на странице отображается подсказка 'В корзине нет товаров, к которым можно применить введенный промокод'"):
        expect(checkout_page.promo_code_field_info()).to_have_text("В корзине нет товаров, к которым можно применить введенный промокод")


@pytest.mark.auth
@allure.title("Отмена промокода")
def test_checkout_canceling_promo_code(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.check_promo_code()
    with allure.step("Запоминю цену товара до активации промокода"):
        pre_action_price = checkout_page.base_price()
    checkout_page.activate_valid_promo_code()
    checkout_page.cancel_promo_code()
    with allure.step("Запоминую цену товара после отмены промокода"):
        post_action_price = checkout_page.base_price()
    with allure.step("Проверяю, что цена до ативации промокода и после его отмены -равны"):
        assert pre_action_price == post_action_price
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(checkout_page.promo_code_field()).to_have_attribute("data-empty", "true")


@pytest.mark.auth
@allure.title("Очистка поля 'Промокод'")
def test_checkout_cleaning_intput_promo_code(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.check_promo_code()
    checkout_page.fill_valid_promo_code()
    checkout_page.clear_promo_code_field_by_cross()
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(checkout_page.promo_code_field()).to_have_attribute("data-empty", "true")


@pytest.mark.auth
@allure.title("Активация подсказки")
def test_checkout_activating_a_hint(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.check_promo_code()
    checkout_page.hover_to_promo_code_hint()
    with allure.step("Проверяю, что подсказка отображается на странице"):
        expect(checkout_page.promo_code_hint_popup()).to_be_visible()
    with allure.step("Проверяю, что текст подсказки соответствует шаблону"):
        assert checkout_page.promo_code_hint_popup_text() == "Промокод действует на отдельные товары и в ограниченный период времени. Подробные условия действия промокода вы можете узнать в описании акции, при получении промокода или у наших специалистов."

# Методы манипулиции с промкодом
# checkout_page.price_changes_with_a_promo_code()

"""Тесты для блока калькуляции"""


@allure.title("Изменение цены в блоке калькуляции по всем позициям")
def calculation_block_calculate_price_for_all_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    total_price = cart_page.calculate_total_price()
    cart_page.get_cart_prices()
    cart_page.compare_prices(total_price)


@allure.title("Изменение цены в блоке калькуляции по части позиций (Чек-бокс)")
def calculation_block_calculate_price_of_some_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.order_price_is_zero()
    cart_page.click_first_checkbox_product()
    cart_page.calculate_total_price_for_checked_products()
    cart_page.click_second_checkbox_product()
    cart_page.calculate_total_price_for_checked_products()


@allure.title("Отправка на печать")
def cart_print_form_activation(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_print_button()
    with allure.step("Проверяю, что окно печати на странице"):
        page_fixture.wait_for_function("window.waitForPrintDialog")


@allure.title("Изменение количества товара через счетчик")
def cart_counter(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    with allure.step("Проверяю, что количество товара меняется"):
        with allure.step("Проверяю, что количество выбранной позиции = 1"):
            quantity = cart_page.get_quantity_of_product()
            assert quantity[0] == 1
        with allure.step("Увеличиваю количество товара на 1"):
            page_fixture.locator(".Counter__Element").nth(1).click()
        with allure.step("Проверяю, что количество выбранной позиции = 2"):
            quantity = cart_page.get_quantity_of_product()
            assert quantity[0] == 2
        with allure.step("Уменьшаю количество товара на 1"):
            page_fixture.locator(".Counter__Element").nth(0).click()
        with allure.step("Проверяю, что количество выбранной позиции = 1"):
            quantity = cart_page.get_quantity_of_product()
            assert quantity[0] == 1


@allure.title("Изменение цены в блоке калькуляции по части позиций (Счетчик)")
def cart_calculation_block_calculate_price_of_some_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    with allure.step("Запоминаю цену товара"):
        price_text = page_fixture.locator('.AvailableList.CartPage__AvailableProductList .Price__Value').nth(0).inner_text()
        price = int(price_text.replace('\xa0', '').replace(' ', ''))
    with allure.step("Запоминаю общую сумму заказа"):
        total_price = cart_page.order_total_price()
    with allure.step("Проверяю, что цена товара соответствует сумме заказа"):
        assert price == total_price
    with allure.step("Увеличиваю количество товара на 1"):
        page_fixture.locator(".Counter__Element").nth(1).click()  #первый плюс
    with allure.step("Считаю стоимость товара в колличестве 2-х единиц"):
        new_price = price+price
    with allure.step("Запоминаю суму заказа"):
        total_price = cart_page.order_total_price()
    with allure.step("Проверяю, что стоимость двух товаров равняется сумме заказа"):
        assert new_price == total_price
    with allure.step("Уменьшаю количество товара на 1"):
        page_fixture.locator(".Counter__Element").nth(0).click()  # первый плюс
    with allure.step("Проверяю, что сумма заказа равна сумме одной единице товара"):
        total_price = cart_page.order_total_price()
        assert price == total_price