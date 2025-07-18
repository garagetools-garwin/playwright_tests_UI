"""В этом файле хранятся тесты для чекаут"""
import re
import time

import pytest
import allure

from playwright.sync_api import expect

from conftest import delete_recipient_fixture
from page_objects.checkout_page import CheckoutPage
from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.companies_page import CompaniesPage
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
    checkout_page.promo_code.check_promo_code()
    with allure.step("Запоминю цену товара до активации промокода"):
        base_price = checkout_page.delivery_block.base_price()
        checkout_page.promo_code.activate_valid_promo_code()
    with allure.step("Запоминаю цену товара после активации промокода"):
        discounted_price = checkout_page.delivery_block.base_price()
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
    checkout_page.promo_code.check_promo_code()
    with allure.step("Запоминю цену товара до активации промокода"):
        pre_action_price = checkout_page.delivery_block.base_price()
        checkout_page.promo_code.activate_invalid_promo_code()
    with allure.step("Запоминаю цену товара после активации промокода"):
        post_action_price = checkout_page.delivery_block.base_price()
    with allure.step("Проверяю, что цена товара не изменилась"):
        assert pre_action_price == post_action_price
    with allure.step("Проверяю, что на странице отображается подсказка 'Промокод не действителен'"):
        expect(checkout_page.promo_code.promo_code_field_info()).to_have_text("Промокод не действителен")


@pytest.mark.auth
@allure.title("Раскрытие блока 'Промокод'")
def test_checkout_promo_code_block(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.promo_code.open_promo_code_bar()
    with allure.step("Запоминаю положение блока 'Промокод'"):
        promo_code_bar_status = checkout_page.promo_code.promo_code_bar()
    with allure.step("Проверяю, что блок 'Промокод' - раскрыт "):
        expect(promo_code_bar_status).to_have_class('PromoWidget__ToggleButton --is-active')
    checkout_page.promo_code.close_promo_code_bar()
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
    checkout_page.promo_code.check_promo_code()
    checkout_page.promo_code.activate_valid_promo_code()
    with allure.step("Проверяю, что на странице отображается подсказка 'В корзине нет товаров, к которым можно применить введенный промокод'"):
        expect(checkout_page.promo_code.promo_code_field_info()).to_have_text("В корзине нет товаров, к которым можно применить введенный промокод")


@pytest.mark.auth
@allure.title("Отмена промокода")
def test_checkout_canceling_promo_code(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.promo_code.check_promo_code()
    with allure.step("Запоминю цену товара до активации промокода"):
        pre_action_price = checkout_page.delivery_block.base_price()
    checkout_page.promo_code.activate_valid_promo_code()
    checkout_page.promo_code.cancel_promo_code()
    with allure.step("Запоминую цену товара после отмены промокода"):
        post_action_price = checkout_page.delivery_block.base_price()
    with allure.step("Проверяю, что цена до ативации промокода и после его отмены -равны"):
        assert pre_action_price == post_action_price
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(checkout_page.promo_code.promo_code_field()).to_have_attribute("data-empty", "true")


@pytest.mark.auth
@allure.title("Очистка поля 'Промокод'")
def test_checkout_cleaning_intput_promo_code(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.promo_code.check_promo_code()
    checkout_page.promo_code.fill_valid_promo_code()
    checkout_page.promo_code.clear_promo_code_field_by_cross()
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(checkout_page.promo_code.promo_code_field()).to_have_attribute("data-empty", "true")


@pytest.mark.auth
@allure.title("Активация подсказки")
def test_checkout_activating_a_hint(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.open(base_url)
    checkout_page.promo_code.check_promo_code()
    checkout_page.promo_code.hover_to_promo_code_hint()
    with allure.step("Проверяю, что подсказка отображается на странице"):
        expect(checkout_page.promo_code.promo_code_hint_popup()).to_be_visible()
    with allure.step("Проверяю, что текст подсказки соответствует шаблону"):
        assert checkout_page.promo_code.promo_code_hint_popup_text() == "Промокод действует на отдельные товары и в ограниченный период времени. Подробные условия действия промокода вы можете узнать в описании акции, при получении промокода или у наших специалистов."

# Методы манипулиции с промкодом
# checkout_page.price_changes_with_a_promo_code()

"""Тесты для блоков Калькуляция и Доставка"""

@pytest.mark.auth
@allure.title("Итоговая стоимость заказа с промокодом и доставкой")
def test_total_cost_with_promo_code_and_shipping(page_fixture, base_url, delete_address_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_not_discounted_product(base_url)
    checkout_page.obtaining_block.create_address(base_url, page_fixture)
    delete_address_fixture()
    with allure.step("Проверяю, что стоимость доставки отображается в блоке калькуляции"):
        assert checkout_page.calculation_block.delivery_price() == checkout_page.delivery_block.delivery_price()

    checkout_page.promo_code.check_promo_code()
    checkout_page.promo_code.activate_valid_promo_code()

    with allure.step("Проверяю, что итоговая сумма считается с учетом скидки и стоимости доставки"):
        total_price = checkout_page.calculation_block.total_price_value()
        delivery_price = checkout_page.calculation_block.delivery_price()
        discount_price = checkout_page.calculation_block.discount_price()
        products_price = checkout_page.calculation_block.products_price()
        assert total_price == products_price + delivery_price - discount_price


@pytest.mark.auth
@allure.title("Итоговая стоимость заказа со скидкой по акции")
def test_total_cost_with_promo_product(page_fixture, base_url, delete_address_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_promo_product(base_url, page_fixture)
    checkout_page.obtaining_block.create_address_pvz_garwin(base_url, page_fixture)
    delete_address_fixture()
    checkout_page.open(base_url)

    with allure.step("Проверяю, что итоговая сумма считается с учетом скидки и стоимости доставки"):
        total_price = checkout_page.calculation_block.total_price_value()
        discount_price = checkout_page.calculation_block.discount_price()
        products_price = checkout_page.calculation_block.products_price()
        assert total_price == products_price - discount_price


@pytest.mark.auth_empty
@allure.title("Кнопка Оформить заказ не активна если у пользователя не выбран получатель и адрес")
def test_place_an_order_button_disabled_without_recipient_and_adress(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_promo_product(base_url, page_fixture)
    checkout_page.open(base_url)

    with allure.step("Проверяю, что кнопка Оформить заказ не активна"):
        order_button_status = checkout_page.calculation_block.order_button_status()
        expect(order_button_status).to_be_disabled()

@pytest.mark.auth
@allure.title("Переход на страницы Политика конфиденциальности и Договор-оферта")
def test_navigating_to_user_documentation_pages(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_promo_product(base_url, page_fixture)
    checkout_page.obtaining_block.create_address_pvz_garwin(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    checkout_page.calculation_block.click_privacy_policy()
    with allure.step("Проверяю, что переход на ожидаемую страницу прошел успешно"):
        expect(page_fixture).to_have_url(f'{base_url}/web-customer-terms')                                # Проверяем, что URL осответствует заданному
        response = page_fixture.request.get(f'{base_url}/web-customer-terms')                             # Отправляем гет запрос, заводим переменную
        expect(response).to_be_ok()
    checkout_page.open(base_url)
    checkout_page.calculation_block.click_offer_contract()
    with allure.step("Проверяю, что переход на ожидаемую страницу прошел успешно"):
        expect(page_fixture).to_have_url(f'{base_url}/oferta')                                # Проверяем, что URL осответствует заданному
        response = page_fixture.request.get(f'{base_url}/oferta')                             # Отправляем гет запрос, заводим переменную
        expect(response).to_be_ok()

@pytest.mark.auth
@allure.title("При достижении определенной суммы стоимость доставки равна 0")
def test_free_delivery_for_retail(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_product_for_free_delivery(base_url)
    cart_page.open(base_url)
    cart_page.increase_quantity_of_product()
    checkout_page.open(base_url)
    checkout_page.obtaining_block.create_address(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    with allure.step("Проверяю, что что в блоке достака стоит бесплатно"):
        delivery_price = checkout_page.delivery_block.delivery_price()
        assert str(delivery_price) == "бесплатно"
    with allure.step("Проверяю, что что в блоке Итого стоит бесплатно"):
        delivery_price = checkout_page.calculation_block.delivery_price()
        assert str(delivery_price) == "бесплатно"
    cart_page.open(base_url)
    cart_page.reduse_quantity_of_product()
    checkout_page.open(base_url)
    with allure.step("Проверяю, что что в блоке достака стоит бесплатно"):
        delivery_price = checkout_page.delivery_block.delivery_price()
        assert str(delivery_price) != "бесплатно"
    with allure.step("Проверяю, что что в блоке Итого стоит бесплатно"):
        delivery_price = checkout_page.calculation_block.delivery_price()
        assert str(delivery_price) != "бесплатно"


@pytest.mark.auth
@allure.title("Стоимость доставки не определена")
def test_delivery_cost_not_determined(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.create_address_pvz_garwin(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    with allure.step("Проверяю, что в блоке доставки стоимость доставки определена как Уточнить у менеджера"):
        delivery_price = checkout_page.delivery_block.delivery_price()
        assert str(delivery_price) == "Уточнить у менеджера"
    with allure.step("Проверяю, что в блоке Итого стоимость доставки не определена"):
        delivery_price = checkout_page.calculation_block.delivery_price()
        assert str(delivery_price) == "не определена"

        """Блок Покупатель и получатель"""

@pytest.mark.auth
@allure.title("Добавление нового получателя со всеми полями")
def test_add_new_recipient_with_all_fields(page_fixture, base_url, delete_recipient_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.add_recipient_modal.add_recipient_modal_open()
    name, phone, email = checkout_page.add_recipient_modal.fill_in_data_randomize()
    checkout_page.add_recipient_modal.click_save_new_recipient_button()
    with allure.step("Проверяю, что модальное окно нового пользователя закрыто"):
        expect(checkout_page.add_recipient_modal.add_recipient_modal_()).not_to_be_visible()
    with allure.step("Проверяю, что листинг пользователей закрыт"):
        expect(checkout_page.recipient_listing.recipient_listing_modal()).not_to_be_visible()
    delete_recipient_fixture()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = f"{email}, {phone}"
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)

@pytest.mark.auth
@allure.title("Добавление нового получателя только с обязательными полями")
def test_add_new_recipient_with_part_of_the_fields(page_fixture, base_url, delete_recipient_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.add_recipient_modal.add_recipient_modal_open()
    name, phone = checkout_page.add_recipient_modal.fill_in_name_and_phone_data_randomize()
    checkout_page.add_recipient_modal.click_save_new_recipient_button()
    delete_recipient_fixture()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = phone
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)

@pytest.mark.auth
@allure.title("Создание нового получателя со всеми валидными символами в ФИО")
def test_add_new_recipient_with_name_with_all_valid_simbols(page_fixture, base_url,delete_recipient_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.add_recipient_modal.add_recipient_modal_open()
    with allure.step("Ввожу текст в котором включены все допустимые буквы и символы, их максимальное количество"):
        name, phone, email = checkout_page.add_recipient_modal.fill_in_data()
    checkout_page.add_recipient_modal.click_save_new_recipient_button()
    delete_recipient_fixture()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = f"{email}, {phone}"
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)

@pytest.mark.auth
@allure.title("Закрытие окна Новый получатель через крестик")
def test_add_new_recipient_close_madal1(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.add_recipient_modal.add_recipient_modal_open()
    checkout_page.add_recipient_modal.close_new_recipient_modal()

@pytest.mark.auth
@allure.title("Закрытие окна Новый получатель через нажатие на пространство вне окна")
def test_add_new_recipient_close_madal2(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.add_recipient_modal.add_recipient_modal_open()
    checkout_page.add_recipient_modal.close_new_recipient_modal2()

@pytest.mark.auth_empty
@allure.title("Открытие модального окна Новый получатель через блок Покупатель и получатель")
def test_open_add_recipient_from_checkout(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.buyer_and_recipient_block.click_add_first_recipient_button()

    with allure.step("Проверяю, что модальное окно Новый получатель - открыто"):
        expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()


"""Листинг получателей"""

@pytest.mark.auth
@allure.title("Открытие листинга получателей (через кнопку Изменить)")
def test_recipient_listing_activation(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    with allure.step("Провряю, что листинг получателей отображается на странице"):
        expect(checkout_page.recipient_listing.recipient_listing_modal()).to_be_visible()


@pytest.mark.auth
@allure.title("Выбор нового получателя")
def test_select_a_new_recipient(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.switch_on_inactive_recipient()
    checkout_page.recipient_listing.select_inactive_recipient()


@pytest.mark.auth
@allure.title("Активация окна Изменить получателя")
def test_activate_the_change_recipient_modal(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()


@pytest.mark.auth
@allure.title("Активация окно подтверждения удаления")
def test_activate_delete_confirmation_modal_recipient(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_delete_button()


"""Модальное окно подтверждения удаления"""

#TODO: удалить paramitrize и удалить run из функции
@pytest.mark.auth
@allure.title("Удаление получателя")
# @pytest.mark.parametrize("run", range(220)) # добавить run в параметры функции
def test_deletion_recipient(page_fixture, base_url, delete_recipient_fixture):
    checkout_page = CheckoutPage(page_fixture)
    # cart_page = CartPage(page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_recipient_fixture()
    # cart_page.open(base_url)
    # cart_page.clear_cart()
    # cart_page.add_to_cart(base_url)
    # checkout_page.open(base_url)
    # checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    # checkout_page.recipient_listing.open_action_menu()
    # checkout_page.delete_conformation_modal.delete_recipient()


@pytest.mark.auth
@allure.title("Отмена удаления получателя")
def test_cancel_recipient_deletion(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.delete_conformation_modal.cancel_recipient_deletion(base_url, page_fixture)


@pytest.mark.auth
@allure.title("Закрытие окна удаления получателя")
def test_close_recipient_deletion_modal(page_fixture, base_url, delete_recipient_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_recipient_fixture()
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.delete_conformation_modal.close_recipient_deletion_modal(base_url, page_fixture)


"""Модальное окно Изменить получателя"""


@pytest.mark.auth
@allure.title("Открытие окна Изменить получателя")
def test_open_recipient_edit_modal(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()

@pytest.mark.auth
@allure.title("Изменение всех полей получателя")
def test_change_recipient_with_all_fields(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    name, phone, email = checkout_page.edit_recipient_modal.fill_in_data_randomize()
    checkout_page.edit_recipient_modal.click_save_edited_recipient_button()
    with allure.step("Проверяю, что модальное окно нового пользователя закрыто"):
        expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).not_to_be_visible()
    with allure.step("Проверяю, что листинг пользователей закрыт"):
        expect(checkout_page.recipient_listing.recipient_listing_modal()).not_to_be_visible()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = f"{email}, {phone}"
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)

@pytest.mark.auth
@allure.title("Изменение только обязательных полей получателя")
def test_edit_part_of_the_fields_of_recipient(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    name, phone = checkout_page.edit_recipient_modal.fill_in_name_and_phone_data_randomize()
    email = checkout_page.edit_recipient_modal.save_email()
    checkout_page.edit_recipient_modal.click_save_edited_recipient_button()
    with allure.step("Формирую ожидаемый текст"):
        # Если имейла нет, формируем ожидаемый результат без него
        if email:
            expected_info = f"{name}, {email}, {phone}"
        else:
            expected_info = f"{name}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        if email:
            expected_info_description = f"{email}, {phone}"
        else:
            expected_info_description = phone
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)

@pytest.mark.auth
@allure.title("Изменение получателя со всеми валидными символами в ФИО")
def test_edit_recipient_with_name_with_all_valid_simbols(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    with allure.step("Ввожу текст в котором включены все допустимые буквы и символы, их максимальное количество"):
        name, phone, email = checkout_page.edit_recipient_modal.fill_in_data()
    checkout_page.edit_recipient_modal.click_save_edited_recipient_button()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = f"{email}, {phone}"
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)


@pytest.mark.auth
@allure.title("Закрытие окна Изменить получателя через крестик")
def test_edit_recipient_close_madal1(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    checkout_page.edit_recipient_modal.close_edit_recipient_modal()


@pytest.mark.auth
@allure.title("Закрытие окна Изменить получателя через нажатие на пространство вне окна")
def test_edit_recipient_close_madal2(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    checkout_page.edit_recipient_modal.close_edit_recipient_modal2()


"""Блок Получение"""

"""Листинг адресов"""


@pytest.mark.auth
@allure.title("Открытие карт")
def test_map_opening(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.click_add_adress_button()
    with allure.step("Проверяю, что карты отображается на странице"):
        expect(checkout_page.map.map_modal()).to_be_visible()


@pytest.mark.auth
@allure.title("Добавление ПВЗ")
def test_pickup_point_adding(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.click_add_adress_button()

    with allure.step("Проверяю, что кнопка Пункт выдачи предвыбрана"):
        expect(checkout_page.map.pickup_point_button_status()).to_have_class(
            'CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')

    # Выбор ПВЗ с кастомным событием
    pickup_point_id = "75048c93-dfb2-422d-b17b-ff95ad2193c8"
    target_lat = 59.88164
    target_lon = 30.273926
    checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)

    with allure.step("Проверяю, что точка выбрана (отображается кнопка Забиру здесь)"):
        expect(checkout_page.map.pick_up_here_button()).to_be_visible()

    with allure.step("Запоминаю адрес ПВЗ в модальном окне Карты"):
        map_modal_adress = checkout_page.map.pickup_point_adress().inner_text()

    checkout_page.map.click_pick_up_here_button()
    delete_address_fixture()

    with allure.step("Запоминаю адрес ПВЗ в блоке Получение"):
        obtaining_block_adress = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Проверяю, что в блоке Получения установлися адресс выбранного ПВЗ"):
        assert map_modal_adress == obtaining_block_adress

    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)

    checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)

@pytest.mark.auth
@allure.title("Редактирование ПВЗ")
def test_pickup_point_editing(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)

    with allure.step("Создаю новый адрес"):
        checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
        checkout_page.adress_listing.click_add_adress_button()

        # Выбор ПВЗ с кастомным событием
        pickup_point_id = "75048c93-dfb2-422d-b17b-ff95ad2193c8"
        target_lat = 59.88164
        target_lon = 30.273926
        checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)
        checkout_page.map.click_pick_up_here_button()
        delete_address_fixture()

    with allure.step("Редактирую адрес"):
        checkout_page.obtaining_block.pickup_point_adress_listing_activation()
        checkout_page.adress_listing.open_action_menu()
        checkout_page.adress_listing.click_edit_button()

        with allure.step("Проверяю, что на странице отображается карточка ПВЗ"):
            expect(checkout_page.map.pickup_point_card_info()).to_be_visible()

        # Выбор ПВЗ с кастомным событием
        pickup_point_id = "62e10ad2-164c-4e9e-9e73-f4f096cdddb1"
        target_lat = 59.880017
        target_lon = 30.395683
        checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)

        with allure.step("Проверяю, что адрес соответствует ожидаемому"):
            expect(checkout_page.map.pickup_point_adress()).to_have_text("г Санкт-Петербург, ул Софийская, д 14 к 2б")

        with allure.step("Запоминаю адрес ПВЗ в модальном окне Карты"):
            map_modal_adress = checkout_page.map.pickup_point_adress().inner_text()

        checkout_page.map.click_pick_up_here_button()

        with allure.step("Запоминаю адрес ПВЗ в блоке Получение"):
            obtaining_block_adress = checkout_page.obtaining_block.pickup_point_adress().inner_text()

        with allure.step("Проверяю, что в блоке Получения установлися адресс выбранного ПВЗ"):
            assert map_modal_adress == obtaining_block_adress

        checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)

        checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)



@pytest.mark.auth
@allure.title("Добавление адреса курьера")
def test_courier_adress_adding(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.click_add_adress_button()
    checkout_page.map.click_courier_button()

    with allure.step("Проверяю, что появилось поле Адрес"):
        expect(checkout_page.map.adress_textaria_status()).to_be_visible()

    with allure.step("Ввожу адрес в поле Адрес"):
        checkout_page.map.type_in_textaria("г Санкт-Петербург, ул Ленина, д 31")

    with allure.step("Запоминаю адрес в модальном окне Карты"):
        map_modal_adress = checkout_page.map.text_from_first_adress_in_list().inner_text()

    checkout_page.map.click_first_adress_in_list()
    checkout_page.map.click_pick_up_here_button()
    delete_address_fixture()

    with allure.step("Запоминаю адрес в блоке Получение"):
        obtaining_block_adress = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Проверяю, что в блоке Получения установлися выбранный адрес"):
        assert map_modal_adress == obtaining_block_adress

    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)


@pytest.mark.auth
@allure.title("Редактирование адреса курьера")
def test_courier_adress_editing(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)

    with allure.step("Создаю новый адрес"):
        checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
        checkout_page.adress_listing.click_add_adress_button()
        checkout_page.map.click_courier_button()

        with allure.step("Ввожу адрес в поле Адрес"):
            checkout_page.map.type_in_textaria("Санкт-Петербург, Невский проспект, 64")

        checkout_page.map.click_first_adress_in_list()
        checkout_page.map.click_pick_up_here_button()
        delete_address_fixture()

        with allure.step("Запоминаю адрес в блоке Получение"):
            obtaining_block_adress_first = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Редактирую адрес"):
        checkout_page.obtaining_block.courier_adress_listing_activation()
        checkout_page.adress_listing.open_action_menu()
        checkout_page.adress_listing.click_edit_button()
        checkout_page.map.type_in_textaria("г Санкт-Петербург, ул Ленина, д 31")

        with allure.step("Запоминаю адрес в модальном окне Карты"):
            map_modal_adress = checkout_page.map.text_from_first_adress_in_list().inner_text()

        checkout_page.map.click_first_adress_in_list()
        checkout_page.map.click_pick_up_here_button()

    with allure.step("Запоминаю адрес в блоке Получение"):
        obtaining_block_adress_second = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Проверяю, что в блоке Получения установлися выбранный адрес"):
        assert map_modal_adress == obtaining_block_adress_second

    with allure.step("Проверяю, что новый адрес отличается от предыдушего"):
        assert obtaining_block_adress_first != obtaining_block_adress_second

    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)


@pytest.mark.auth
@allure.title("Редактирование адреса курьера с дополнительной информацией")
def test_courier_adress_editing_with_additional_fields(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)

    with allure.step("Создаю новый адрес"):
        checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
        checkout_page.adress_listing.click_add_adress_button()
        checkout_page.map.click_courier_button()

        with allure.step("Ввожу адрес в поле Адрес"):
            checkout_page.map.type_in_textaria("Санкт-Петербург, Невский проспект, 64")

        checkout_page.map.click_first_adress_in_list()

        with allure.step("Заполняю дополнительные поля"):
            aprtment, entryway, floor, intercom, commentary = checkout_page.map.filling_in_additional_fields()

        checkout_page.map.click_pick_up_here_button()

        delete_address_fixture()

        with allure.step("Формирую данные для сравнения"):
            adress = checkout_page.obtaining_block.check_out_adress()
            expected_data_listing = f"{adress}, Домофон {intercom}, Кв. {aprtment}, Этаж {floor}, Подъезд {entryway}"
            # expected_data_map_modal =

    with allure.step("Редактирую адрес"):
        checkout_page.obtaining_block.courier_adress_listing_activation()

        with allure.step("Проверю, что вся дополнительная информация отображается в листинге адресов"):
            actual_listing_adress = checkout_page.adress_listing.get_selected_adress_info()
            assert expected_data_listing == actual_listing_adress

        checkout_page.adress_listing.open_action_menu()
        checkout_page.adress_listing.click_edit_button()

        # Проверяю что значение каждого поля соотвествует задуманному
        map_aprtment, map_entryway, map_floor, map_intercom, map_commentary = checkout_page.map.get_additional_fields_info()
        assert (map_aprtment, map_entryway, map_floor, map_intercom, map_commentary) == (
        aprtment, entryway, floor, intercom, commentary), (
            f"Значения полей не совпадают! Ожидалось: {(aprtment, entryway, floor, intercom, commentary)}, "
            f"Фактически: {(map_aprtment, map_entryway, map_floor, map_intercom, map_commentary)}"
        )

        checkout_page.map.type_in_textaria("г Санкт-Петербург, ул Ленина, д 31")

        checkout_page.map.click_first_adress_in_list()

        with allure.step("Заполняю дополнительные поля"):
            aprtment, entryway, floor, intercom, commentary = checkout_page.map.filling_in_additional_fields()

        checkout_page.map.click_pick_up_here_button()

    with allure.step("Формирую данные для сравнения"):
        adress = checkout_page.obtaining_block.check_out_adress()
        expected_data_listing = f"{adress}, Домофон {intercom}, Кв. {aprtment}, Этаж {floor}, Подъезд {entryway}"

    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)

    with allure.step("Проверю, что вся дополнительная информация отображается в листинге адресов"):
        actual_listing_adress = checkout_page.adress_listing.get_selected_adress_info()
        assert expected_data_listing == actual_listing_adress

@pytest.mark.auth
@allure.title("Активация окна Удалить адрес")
def test_activate_delete_confirmation_modal_obtaining(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.open_action_menu()
    checkout_page.adress_listing.click_delete_button()


@pytest.mark.auth
@allure.title("Удаление адреса")
# @pytest.mark.parametrize("run", range(140))
def test_deletion_adress(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.click_add_adress_button()

    # Выбор ПВЗ с кастомным событием
    pickup_point_id = "75048c93-dfb2-422d-b17b-ff95ad2193c8"
    target_lat = 59.88164
    target_lon = 30.273926
    checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)

    checkout_page.map.click_pick_up_here_button()
    delete_address_fixture()


@pytest.mark.auth
@allure.title("Выбор нового адреса")
def test_select_a_new_adress(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.switch_on_inactive_adress()
    checkout_page.adress_listing.select_inactive_adress()


@pytest.mark.auth
@allure.title("Переход в листинг адресов через кнопку Пункт выдачи")
def test_adress_listing_activation_from_pickup_point_button(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.pickup_point_adress_listing_activation()
    checkout_page.adress_listing.check_all_pickup_points()


@pytest.mark.auth
@allure.title("Переход в листинг адресов через кнопку Курьер")
def test_adress_listing_activation_from_courier_button(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.courier_adress_listing_activation()
    checkout_page.adress_listing.check_all_courier_adress()


@pytest.mark.auth
@allure.title("Переход в карты через листинг адресов курьера")
def test_courier_button_preselected(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.courier_adress_listing_activation()
    checkout_page.adress_listing.check_all_courier_adress()
    checkout_page.adress_listing.click_add_adress_button()

    with allure.step("Проверяю, что кнопка Курьером предвыбрана"):
        expect(checkout_page.map.courier_button_status()).to_have_class(
            'CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Отработка кнопки Назад и Домой")
def test_back_button(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.click_add_adress_button()

    with allure.step("Проверяю, что модальное окна Карты - открыто"):
        expect(checkout_page.map.map_modal()).to_be_visible()


    with allure.step("Перехожу на страницу ПВЗ"):
        # Выбор ПВЗ с кастомным событием
        pickup_point_id = "75048c93-dfb2-422d-b17b-ff95ad2193c8"
        target_lat = 59.88164
        target_lon = 30.273926
        checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)

    with allure.step("Возвращаюсь со страницы ПВЗ"):
        checkout_page.map.click_back_button()

    with allure.step("Проверяю, что отображается панель управления модального окна Карты"):
        expect(checkout_page.map.control_panel()).to_be_visible()

    with allure.step("Возвращаюсь с модального окна карты в чек-аут"):
        checkout_page.map.click_back_button()

    with allure.step("Проверяю, что модальное окна Карты - закрыто"):
        expect(checkout_page.map.map_modal()).not_to_be_visible()

    checkout_page.obtaining_block.courier_adress_listing_activation()
    checkout_page.adress_listing.click_add_adress_button()

    with allure.step("Ввожу адрес в поле Адрес"):
        checkout_page.map.type_in_textaria("г Санкт-Петербург, ул Ленина, д 31")

    checkout_page.map.click_first_adress_in_list()

    with allure.step("Возвращаюсь с модального окна карты в чек-аут"):
        checkout_page.map.click_back_button()

    with allure.step("Проверяю, что модальное окна Карты - закрыто"):
        expect(checkout_page.map.map_modal()).not_to_be_visible()

    with allure.step("Перехожу на домашнюю страницу"):
        checkout_page.click_logo_button(base_url)
        with allure.step("Дожидаюсь открытия страницы"):
            page_fixture.wait_for_url(f'{base_url}/')
        with allure.step("Проверяю, что url страницы содержит требуемое значение"):
            expect(page_fixture).to_have_url(f'{base_url}/')
        with allure.step("Проверяю, что статус страницы ok"):
            url = page_fixture.url
            response = page_fixture.request.get(url)
            expect(response).to_be_ok()


@pytest.mark.auth
@allure.title("Открытие листинга адресов пользователем с адресами (через кнопку Изменить)")
def test_adress_listing_activation(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation()
    with allure.step("Провряю, что листинг адресов отображается на странице"):
        expect(checkout_page.adress_listing.adress_listing_modal()).to_be_visible()



"""Тесты для аккаунта без адресов"""


@pytest.mark.auth_empty
@allure.title("Открытие карты через кнопку Выберите способ и адрес получения")
def test_open_map_from_obtaining_block(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.click_first_adress_button()

    with allure.step("Проверяю, что модальное окна Карты - открыто"):
        expect(checkout_page.map.map_modal()).to_be_visible()

    with allure.step("Проверяю, что кнопка Пункт выдачи предвыбрана"):
        expect(checkout_page.map.pickup_point_button_status()).to_have_class(
            'CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')


@pytest.mark.auth_empty
@allure.title("Открытие модального окна Карты через кнопку Пункт выдачи")
def test_open_map_from_pickup_point_button(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.pickup_point_adress_listing_activation()

    with allure.step("Проверяю, что модальное окна Карты - открыто"):
        expect(checkout_page.map.map_modal()).to_be_visible()

    with allure.step("Проверяю, что кнопка Пункт выдачи предвыбрана"):
        expect(checkout_page.map.pickup_point_button_status()).to_have_class(
            'CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')


@pytest.mark.auth_empty
@allure.title("Открытие модального окна Карты через кнопку Курьером")
def test_open_map_from_courier_adress_button(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.courier_adress_listing_activation()

    with allure.step("Проверяю, что модальное окна Карты - открыто"):
        expect(checkout_page.map.map_modal()).to_be_visible()

    with allure.step("Проверяю, что кнопка Курьером предвыбрана"):
        expect(checkout_page.map.courier_button_status()).to_have_class(
            'CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')


"""Тесты для блока Оплата"""

@pytest.mark.auth
@allure.title("Способ 'Оплата при получении' доступен")
def test_payment_on_receipt_enebled(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_promo_product(base_url, page_fixture)
    checkout_page.obtaining_block.create_address_pvz_garwin(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    with allure.step("Проверяю, что кнопка Оплата при получении активна"):
        payment_on_receip_button_status = checkout_page.payment_block.payment_on_receip_button_status()
        expect(payment_on_receip_button_status).to_be_enabled()
    with allure.step("Проверяю, что кнопка Уточнить у менеджера активна"):
        contact_a_manager_button_status = checkout_page.payment_block.contact_a_manager_button_status()
        expect(contact_a_manager_button_status).to_be_enabled()

@pytest.mark.auth
@allure.title("Способ 'Оплата при получении' не доступен")
def test_payment_on_receipt_disabled(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_promo_product(base_url, page_fixture)
    checkout_page.obtaining_block.create_address(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    with allure.step("Проверяю, что кнопка Оплата при получении не активна"):
        payment_on_receip_button_status = checkout_page.payment_block.payment_on_receip_button_status()
        expect(payment_on_receip_button_status).to_be_disabled()
    with allure.step("Проверяю, что кнопка Уточнить у менеджера активна"):
        contact_a_manager_button_status = checkout_page.payment_block.contact_a_manager_button_status()
        expect(contact_a_manager_button_status).to_be_enabled()


@pytest.mark.auth
@allure.title("Способы оплаты Онлайн-оплата и Оплата по счету не доступны")
def test_online_payment_on_receipt_and_payment_by_invoice_disabled(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_product_out_of_stock(base_url)
    checkout_page.obtaining_block.create_address(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    with allure.step("Проверяю, что кнопка Онлайн-оплата не активна"):
        online_payment_button_status = checkout_page.payment_block.online_payment_button_status()
        expect(online_payment_button_status).to_be_disabled()
    with allure.step("Проверяю, что кнопка Оплата по счету не активна"):
        payment_by_invoice_button_status = checkout_page.payment_block.payment_by_invoice_button_status()
        expect(payment_by_invoice_button_status).to_be_disabled()
    with allure.step("Проверяю, что кнопка Уточнить у менеджера активна"):
        contact_a_manager_button_status = checkout_page.payment_block.contact_a_manager_button_status()
        expect(contact_a_manager_button_status).to_be_enabled()


@pytest.mark.auth
@allure.title("Способы оплаты Онлайн-оплата и Оплата по счету доступны")
def test_online_payment_on_receipt_and_payment_by_invoice_enabled(page_fixture, base_url, delete_address_fixture, delete_recipient_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    companies_page.select_company_with_retail_price(base_url)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_product_in_stock(base_url)
    checkout_page.obtaining_block.create_address_infor(base_url, page_fixture)
    checkout_page.buyer_and_recipient_block.create_recipient(base_url, page_fixture)
    delete_address_fixture()
    delete_recipient_fixture()
    with allure.step("Проверяю, что что в блоке достака стоит бесплатно"):
        delivery_price = checkout_page.delivery_block.delivery_price()
        assert str(delivery_price) == "бесплатно"
    with allure.step("Проверяю, что что в блоке Итого стоит бесплатно"):
        delivery_price = checkout_page.calculation_block.delivery_price()
        assert str(delivery_price) == "бесплатно"
    with allure.step("Проверяю, что кнопка Онлайн-оплата активна"):
        online_payment_button_status = checkout_page.payment_block.online_payment_button_status()
        expect(online_payment_button_status).to_be_enabled()
    with allure.step("Проверяю, что кнопка Оплата по счету активна"):
        payment_by_invoice_button_status = checkout_page.payment_block.payment_by_invoice_button_status()
        expect(payment_by_invoice_button_status).to_be_enabled()
    with allure.step("Проверяю, что кнопка Уточнить у менеджера активна"):
        contact_a_manager_button_status = checkout_page.payment_block.contact_a_manager_button_status()
        expect(contact_a_manager_button_status).to_be_enabled()


"""Блок Покупатель и получатель (низкий приоритет)"""


#TODO: Переместить тест в блок "Блок Покупатель и получатель"

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("В блоке отображается название выбранного контрагента")
def test_customer_name(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)
    header = HeaderElement(page_fixture)

    cart_page.open(base_url)
    with allure.step("Запоминаю название компании в хедере"):
        company_name_header = header.company_name_text()
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.open(base_url)
    with allure.step("Запоминаю название компании в чек-ауте"):
        company_name_checkout = checkout_page.buyer_and_recipient_block.customer_name_text()
    with allure.step("Проверяю, что в чек-ауте актуальное имя получателя/название компании"):
        assert company_name_header == company_name_checkout

    companies_page.select_a_company_with_a_different_type_of_pricing(base_url)
    with allure.step("Запоминаю название компании в хедере"):
        company_name_header = header.company_name_text()
    checkout_page.open(base_url)
    with allure.step("Запоминаю название компании в чек-ауте"):
        company_name_checkout = checkout_page.buyer_and_recipient_block.customer_name_text()
    with allure.step("Проверяю, что в чек-ауте актуальное имя получателя/название компании"):
        assert company_name_header == company_name_checkout

#TODO: Переместить тест в блок "Блок Покупатель и получатель"
@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Сохраниение нового получателя с некоретными даными")
def test_add_new_recipient_without_the_required_fields(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)

    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.open(base_url)

    with allure.step("Пытаюсь сохранить пользователя с пустыми полями"):
        checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
        with allure.step("Считаю количество записей в листинге(до попыток сделать запись)"):
            number_of_records_before_saving = checkout_page.recipient_listing.count_number_of_records()

        checkout_page.add_recipient_modal.add_recipient_modal_open()
        checkout_page.add_recipient_modal.click_save_new_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
        assert checkout_page.add_recipient_modal.name_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
        assert checkout_page.add_recipient_modal.phone_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

    with allure.step("Пытаюсь сохранить пользователя только с ФИО"):
        checkout_page.add_recipient_modal.fill_name_data_randomize()
        checkout_page.add_recipient_modal.click_save_new_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО не появилась ошибка"):
        assert checkout_page.add_recipient_modal.name_field_error_text() == ""
    with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
        assert checkout_page.add_recipient_modal.phone_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

    with allure.step("Пытаюсь сохранить пользователя только с номером телефона"):
        checkout_page.add_recipient_modal.clear_all_fields()
        checkout_page.add_recipient_modal.fill_phone_data_randomize()
        checkout_page.add_recipient_modal.click_save_new_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
        assert checkout_page.add_recipient_modal.name_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что под под полем Телефон не появилась ошибка"):
        assert checkout_page.add_recipient_modal.phone_field_error_text() == ""
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

    with allure.step("Пытаюсь сохранить пользователя только с e-mail"):
        checkout_page.add_recipient_modal.clear_all_fields()
        checkout_page.add_recipient_modal.fill_email_data_randomize()
        checkout_page.add_recipient_modal.click_save_new_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
        assert checkout_page.add_recipient_modal.name_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что под под полем Телефон не появилась ошибка"):
        assert checkout_page.add_recipient_modal.phone_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

    with allure.step("Считаю количество записей в листинге(после попыток сделать запись)"):
        checkout_page.add_recipient_modal.close_new_recipient_modal()
        checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
        number_of_records_after_saving = checkout_page.recipient_listing.count_number_of_records()

    with allure.step("Проверяю, что новых записей сделано не было"):
        assert number_of_records_before_saving == number_of_records_after_saving

#TODO: Переместить тест в блок "Блок Покупатель и получатель"
@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Сохраниение нового получателя с некоретными данными")
def test_add_new_recipient_with_incorrect_data(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)

    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.open(base_url)

    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Считаю количество записей в листинге(до попыток сделать запись)"):
        number_of_records_before_saving = checkout_page.recipient_listing.count_number_of_records()

    with allure.step("Проверяю, недопустимые значения для ФИО"):
        with allure.step("Вношу в поле ФИО цифры"):
            checkout_page.add_recipient_modal.add_recipient_modal_open()
            checkout_page.add_recipient_modal.fill_name("590640563432")
            checkout_page.add_recipient_modal.fill_phone_data_randomize()

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
                assert checkout_page.add_recipient_modal.name_field_error_text() == "Допустимы буквы на латинице и кириллице, пробел, дефис, одинарная кавычка. Не более 90 символов."
            with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
                assert checkout_page.add_recipient_modal.phone_field_error_text() == ""
            with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
                expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

        with allure.step("Вношу в поле ФИО нижнее подчеркивание"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name("Оле_г")
            checkout_page.add_recipient_modal.fill_phone_data_randomize()

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
                assert checkout_page.add_recipient_modal.name_field_error_text() == "Допустимы буквы на латинице и кириллице, пробел, дефис, одинарная кавычка. Не более 90 символов."
            with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
                assert checkout_page.add_recipient_modal.phone_field_error_text() == ""
            with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
                expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

        with allure.step("Вношу в поле ФИО более 90 символов"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name("Здесь находится текст из более чем девяноста символов для проверки поля ФИО на максимальное количество допустимых символов")
            checkout_page.add_recipient_modal.fill_phone_data_randomize()

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
                assert checkout_page.add_recipient_modal.name_field_error_text() == "Допустимы буквы на латинице и кириллице, пробел, дефис, одинарная кавычка. Не более 90 символов."
            with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
                assert checkout_page.add_recipient_modal.phone_field_error_text() == ""
            with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
                expect(checkout_page.add_recipient_modal.add_recipient_modal_()).to_be_visible()

    with allure.step("Проверяю, недопустимые значения для поля email"):
        with allure.step("Вношу в поле email два символа '@'"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name_data_randomize()
            checkout_page.add_recipient_modal.fill_phone_data_randomize()
            checkout_page.add_recipient_modal.fill_email("test@@mail.com")

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под полем E-mail появилась ошибка при двух символах '@'"):
                assert checkout_page.add_recipient_modal.email_field_error_text() == "Некорректный формат e-mail."

        with allure.step("Не вношу в поле email символ '@'"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name_data_randomize()
            checkout_page.add_recipient_modal.fill_phone_data_randomize()
            checkout_page.add_recipient_modal.fill_email("testmail.com")

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под полем E-mail появилась ошибка при отсутствии '@'"):
                assert checkout_page.add_recipient_modal.email_field_error_text() == "Некорректный формат e-mail."

        with allure.step("Не вношу в поле email символ '.'"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name_data_randomize()
            checkout_page.add_recipient_modal.fill_phone_data_randomize()
            checkout_page.add_recipient_modal.fill_email("test@mailcom")

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под полем E-mail появилась ошибка при отсутствии '.'"):
                assert checkout_page.add_recipient_modal.email_field_error_text() == "Некорректный формат e-mail."

    with allure.step("Проверяю, недопустимые значения для поля Телефон"):
        with allure.step("Вношу в поле Телефон латинские и кирилические буквы"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name_data_randomize()
            checkout_page.add_recipient_modal.fill_phone("abcABCабвАБВ")
            checkout_page.add_recipient_modal.fill_email_data_randomize()

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под полем Телефон появилась ошибка при вводе букв"):
                assert checkout_page.add_recipient_modal.phone_field_error_text() == "Некорректный формат телефона."

        with allure.step("Вношу в поле Телефон только одну цифру"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name_data_randomize()
            checkout_page.add_recipient_modal.fill_phone("7")
            checkout_page.add_recipient_modal.fill_email_data_randomize()

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под полем Телефон появилась ошибка при вводе 1 символа"):
                assert checkout_page.add_recipient_modal.phone_field_error_text() == "Некорректный формат телефона."

        with allure.step("Вношу в поле Телефон на одну цифру меньше валидного (требуется 10)"):
            checkout_page.add_recipient_modal.clear_all_fields()
            checkout_page.add_recipient_modal.fill_name_data_randomize()
            checkout_page.add_recipient_modal.fill_phone("79991234")
            checkout_page.add_recipient_modal.fill_email_data_randomize()

            checkout_page.add_recipient_modal.click_save_new_recipient_button()

            with allure.step("Проверяю, что под полем Телефон появилась ошибка при неполном номере"):
                assert checkout_page.add_recipient_modal.phone_field_error_text() == "Некорректный формат телефона."

    with allure.step("Считаю количество записей в листинге(после попыток сделать запись)"):
        checkout_page.add_recipient_modal.close_new_recipient_modal()
        checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
        number_of_records_after_saving = checkout_page.recipient_listing.count_number_of_records()

    with allure.step("Проверяю, что новых записей сделано не было"):
        assert number_of_records_before_saving == number_of_records_after_saving

#TODO: Переместить тест в блок "Изменить получателя"

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Меняю данные получателя на некорректные")
def test_edit_recipient_without_the_required_fields(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)

    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.open(base_url)

    with allure.step("Пытаюсь сохранить пользователя с пустыми полями"):
        checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

        with allure.step("Запоминаю данные получателя до попыток его отредактировать"):
            name_of_first_recipient_before = checkout_page.recipient_listing.name_of_first_recipient()
            phone_and_email_of_first_recipient_before = checkout_page.recipient_listing.phone_and_email_of_first_recipient()

        checkout_page.recipient_listing.open_action_menu()
        checkout_page.recipient_listing.click_edit_button()
        checkout_page.edit_recipient_modal.clear_all_fields()
        checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
        assert checkout_page.edit_recipient_modal.name_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
        assert checkout_page.edit_recipient_modal.phone_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()

    with allure.step("Пытаюсь сохранить пользователя только с ФИО"):
        checkout_page.edit_recipient_modal.fill_name_data_randomize()
        checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО не появилась ошибка"):
        assert checkout_page.edit_recipient_modal.name_field_error_text() == ""
    with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
        assert checkout_page.edit_recipient_modal.phone_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()

    with allure.step("Пытаюсь сохранить пользователя только с номером телефона"):
        checkout_page.edit_recipient_modal.clear_all_fields()
        checkout_page.edit_recipient_modal.fill_phone_data_randomize()
        checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
        assert checkout_page.edit_recipient_modal.name_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что под под полем Телефон не появилась ошибка"):
        assert checkout_page.edit_recipient_modal.phone_field_error_text() == ""
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()

    with allure.step("Пытаюсь сохранить пользователя только с e-mail"):
        checkout_page.edit_recipient_modal.clear_all_fields()
        checkout_page.edit_recipient_modal.fill_email_data_randomize()
        checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

    with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
        assert checkout_page.edit_recipient_modal.name_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что под под полем Телефон не появилась ошибка"):
        assert checkout_page.edit_recipient_modal.phone_field_error_text() == "Поле обязательно для заполнения"
    with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
        expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()
    checkout_page.edit_recipient_modal.close_edit_recipient_modal()
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Запоминаю данные получателя после попыток его отредактировать"):
        name_of_first_recipient_after = checkout_page.recipient_listing.name_of_first_recipient()
        phone_and_email_of_first_recipient_after = checkout_page.recipient_listing.phone_and_email_of_first_recipient()

    with allure.step("Проверяю, что после всех попыток изменить пользователя, он остался неизменным"):
        assert name_of_first_recipient_before == name_of_first_recipient_after
        assert phone_and_email_of_first_recipient_before == phone_and_email_of_first_recipient_after

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Сохранение нового получателя с некорректным ФИО")
def test_edit_recipient_with_incorrect_data(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)

    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)
    checkout_page.open(base_url)

    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Запоминаю данные получателя до попыток его отредактировать"):
        name_of_first_recipient_before = checkout_page.recipient_listing.name_of_first_recipient()
        phone_and_email_of_first_recipient_before = checkout_page.recipient_listing.phone_and_email_of_first_recipient()

    with allure.step("Проверяю, недопустимые значения для ФИО"):
        with allure.step("Вношу в поле ФИО цифры"):
            checkout_page.recipient_listing.open_action_menu()
            checkout_page.recipient_listing.click_edit_button()
            checkout_page.edit_recipient_modal.fill_name("590640563432")
            checkout_page.edit_recipient_modal.fill_phone_data_randomize()

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
                assert checkout_page.edit_recipient_modal.name_field_error_text() == "Допустимы буквы на латинице и кириллице, пробел, дефис, одинарная кавычка. Не более 90 символов."
            with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
                assert checkout_page.edit_recipient_modal.phone_field_error_text() == ""
            with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
                expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()

        with allure.step("Вношу в поле ФИО нижнее подчеркивание"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name("Оле_г")
            checkout_page.edit_recipient_modal.fill_phone_data_randomize()

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
                assert checkout_page.edit_recipient_modal.name_field_error_text() == "Допустимы буквы на латинице и кириллице, пробел, дефис, одинарная кавычка. Не более 90 символов."
            with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
                assert checkout_page.edit_recipient_modal.phone_field_error_text() == ""
            with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
                expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()

        with allure.step("Вношу в поле ФИО более 90 символов"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name("Здесь находится текст из более чем девяноста символов для проверки поля ФИО на максимальное количество допустимых символов")
            checkout_page.edit_recipient_modal.fill_phone_data_randomize()

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под под полем ФИО появилась ошибка"):
                assert checkout_page.edit_recipient_modal.name_field_error_text() == "Допустимы буквы на латинице и кириллице, пробел, дефис, одинарная кавычка. Не более 90 символов."
            with allure.step("Проверяю, что под под полем Телефон появилась ошибка"):
                assert checkout_page.edit_recipient_modal.phone_field_error_text() == ""
            with allure.step("Проверяю, что модальное окно нового пользователя не закрыто"):
                expect(checkout_page.edit_recipient_modal.edit_recipient_modal()).to_be_visible()

    with allure.step("Проверяю, недопустимые значения для поля email"):
        with allure.step("Вношу в поле email два символа '@'"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name_data_randomize()
            checkout_page.edit_recipient_modal.fill_phone_data_randomize()
            checkout_page.edit_recipient_modal.fill_email("test@@mail.com")

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под полем E-mail появилась ошибка при двух символах '@'"):
                assert checkout_page.edit_recipient_modal.email_field_error_text() == "Некорректный формат e-mail."

        with allure.step("Не вношу в поле email символ '@'"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name_data_randomize()
            checkout_page.edit_recipient_modal.fill_phone_data_randomize()
            checkout_page.edit_recipient_modal.fill_email("testmail.com")

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под полем E-mail появилась ошибка при отсутствии '@'"):
                assert checkout_page.edit_recipient_modal.email_field_error_text() == "Некорректный формат e-mail."

        with allure.step("Не вношу в поле email символ '.'"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name_data_randomize()
            checkout_page.edit_recipient_modal.fill_phone_data_randomize()
            checkout_page.edit_recipient_modal.fill_email("test@mailcom")

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под полем E-mail появилась ошибка при отсутствии '.'"):
                assert checkout_page.edit_recipient_modal.email_field_error_text() == "Некорректный формат e-mail."

    with allure.step("Проверяю, недопустимые значения для поля Телефон"):
        with allure.step("Вношу в поле Телефон латинские и кирилические буквы"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name_data_randomize()
            checkout_page.edit_recipient_modal.fill_phone("abcABCабвАБВ")
            checkout_page.edit_recipient_modal.fill_email_data_randomize()

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под полем Телефон появилась ошибка при вводе букв"):
                assert checkout_page.edit_recipient_modal.phone_field_error_text() == "Некорректный формат телефона."

        with allure.step("Вношу в поле Телефон только одну цифру"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name_data_randomize()
            checkout_page.edit_recipient_modal.fill_phone("7")
            checkout_page.edit_recipient_modal.fill_email_data_randomize()

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под полем Телефон появилась ошибка при вводе 1 символа"):
                assert checkout_page.edit_recipient_modal.phone_field_error_text() == "Некорректный формат телефона."

        with allure.step("Вношу в поле Телефон на одну цифру меньше валидного (требуется 10)"):
            checkout_page.edit_recipient_modal.clear_all_fields()
            checkout_page.edit_recipient_modal.fill_name_data_randomize()
            checkout_page.edit_recipient_modal.fill_phone("79991234")
            checkout_page.edit_recipient_modal.fill_email_data_randomize()

            checkout_page.edit_recipient_modal.click_save_edited_recipient_button()

            with allure.step("Проверяю, что под полем Телефон появилась ошибка при неполном номере"):
                assert checkout_page.edit_recipient_modal.phone_field_error_text() == "Некорректный формат телефона."

    checkout_page.edit_recipient_modal.close_edit_recipient_modal()
    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

    with allure.step("Запоминаю данные получателя после попыток его отредактировать"):
        name_of_first_recipient_after = checkout_page.recipient_listing.name_of_first_recipient()
        phone_and_email_of_first_recipient_after = checkout_page.recipient_listing.phone_and_email_of_first_recipient()

    with allure.step("Проверяю, что после всех попыток изменить пользователя, он остался неизменным"):
        assert name_of_first_recipient_before == name_of_first_recipient_after
        assert phone_and_email_of_first_recipient_before == phone_and_email_of_first_recipient_after

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Ввод валидного адреса курьера")
def test_enter_valid_courier_address(page_fixture, base_url, delete_address_fixture):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
    checkout_page.adress_listing.click_add_adress_button()
    checkout_page.map.click_courier_button()

    with allure.step("Проверяю, что появилось поле Адрес"):
        expect(checkout_page.map.adress_textaria_status()).to_be_visible()

    with allure.step("Ввожу адрес в поле Адрес"):
        checkout_page.map.type_in_textaria("юрия гагарина санкт-петербург")

    with allure.step("Проверяю, что адрес содержит введенные значения"):
        map_modal_adress = checkout_page.map.text_from_first_adress_in_list()
        expect(map_modal_adress).to_have_text(re.compile('Санкт-Петербург'))
        expect(map_modal_adress).to_have_text(re.compile("Юрия Гагарина"))

    with allure.step("Добавляю в адрес номер дома"):
        checkout_page.map.type_in_textaria("юрия гагарина санкт-петербург 11")

    with allure.step("Проверяю, что адрес содержит введенные значения"):
        map_modal_adress = checkout_page.map.text_from_first_adress_in_list()
        expect(map_modal_adress).to_have_text(re.compile("Санкт-Петербург"))
        expect(map_modal_adress).to_have_text(re.compile("Юрия Гагарина"))
        expect(map_modal_adress).to_have_text(re.compile("11"))

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("При переключении покупателя меняется цена в блоках Итого и Доставка")
def test_customer_switching_price(page_fixture, base_url,delete_address_fixture):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    companies_page = CompaniesPage(page_fixture)

    companies_page.select_company_with_retail_price(base_url)

    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_product_in_stock(base_url)
    checkout_page.open(base_url)

    with allure.step("Запоминаю название компании в чек-ауте"):
        company_name_checkout_b = checkout_page.buyer_and_recipient_block.customer_name_text()

    checkout_page.obtaining_block.create_address(base_url, page_fixture)
    delete_address_fixture()

    with allure.step("Запоминаю цены до смены контрагента"):
        # b = before
        total_price_b = checkout_page.calculation_block.total_price_value()
        discount_price_b = checkout_page.calculation_block.discount_price()
        delivery_calculation_price_b = checkout_page.calculation_block.delivery_price()

        delivery_price_b = checkout_page.delivery_block.delivery_price()
        product_price_b = checkout_page.delivery_block.base_price()
        delivery_summ_price_b = checkout_page.delivery_block.delivery_summ_price()

    checkout_page.buyer_listing.open_buyer_listing()
    with allure.step("Проверяю, что листинг покупателей открыт"):
        expect(checkout_page.buyer_listing.buyer_listing()).to_be_visible()

    checkout_page.buyer_listing.switch_a_specific_customer()
    checkout_page.buyer_listing.select_inactive_buyer()

    time.sleep(3)

    with allure.step("Запоминаю цены после смены контрагента"):
        # a = after
        total_price_a = checkout_page.calculation_block.total_price_value()
        discount_price_a = checkout_page.calculation_block.discount_price()
        delivery_calculation_price_a = checkout_page.calculation_block.delivery_price()

        delivery_price_a = checkout_page.delivery_block.delivery_price()
        product_price_a = checkout_page.delivery_block.base_price()
        delivery_summ_price_a = checkout_page.delivery_block.delivery_summ_price()

        company_name_checkout_a = checkout_page.buyer_and_recipient_block.customer_name_text()

    with allure.step("Проверяю что цены изменились"):
        assert total_price_a != total_price_b
        assert discount_price_a != discount_price_b
        assert delivery_calculation_price_a != delivery_calculation_price_b

        assert delivery_price_a != delivery_price_b
        assert product_price_a != product_price_b
        assert delivery_summ_price_a != delivery_summ_price_b

    with allure.step("Проверяю что наименование покупателя сменилось на ожидаемое"):
        assert company_name_checkout_a != company_name_checkout_b
        assert company_name_checkout_a == 'ООО "У КУПЦА"'

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("Закрытие листинга покупателей")
def test_buyer_listing_close_madal(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.buyer_listing.open_buyer_listing()
    checkout_page.buyer_listing.close_buyer_listing_modal1()
    checkout_page.buyer_listing.open_buyer_listing()
    checkout_page.buyer_listing.close_buyer_listing_modal2()

@pytest.mark.test_ci
@pytest.mark.auth
@allure.title("При переключении аккаунта меняется состав контрагентов в чек-ауте")
def test_account_switching_changes_customers(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    checkout_page = CheckoutPage(page_fixture)
    header = HeaderElement(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart_cheap_product(base_url)

    header.switching_to_other_account()

    checkout_page.open(base_url)
    checkout_page.buyer_listing.open_buyer_listing()

    with allure.step("Считаю количество записей в листинге"):
        number_of_customers_before = checkout_page.buyer_listing.counting_the_number_of_customers()
    cart_page.open(base_url)

    header.switching_to_user_account()

    checkout_page.open(base_url)
    checkout_page.buyer_listing.open_buyer_listing()

    with allure.step("Считаю количество записей в листинге"):
        number_of_customers_after = checkout_page.buyer_listing.counting_the_number_of_customers()

    with allure.step("Проверяю, что количестов записей изменилось после переключения аккаунта"):
        assert number_of_customers_before != number_of_customers_after







#TODO: рассмотреть вариант при изменении адреса менять его на ПВЗ и наоборот
#TODO: Вывести все проверки и переменные в тесты
#TODO: написать текст для вывода в отчет в случае падения для каждой проверки
#TODO: написать обработки исключений/ошибок (кинуть запрос в GPT)
#TODO: включить метод открытия корзины в метод очистки корзины
#TODO: написать фикстуру которая будет активироватся при запуске любого теста, считать сколько было создано пулучателей,
# адресов и по завершению всех проиграных тестов удалять требуемое количество сущностей, если их было 0 то фикстура
# просто закончит свою работу. Понадобится расставить флаги после создания сущностей
#TODO: Скидка по промокоду и по акции сново считаются в одном поле, пересмотреть написание тестов связаных с этими полями
#TODO: Убедится, что все сценарии где Уточнить у менеджера и бесплатно в блоке доставка учтены
#TODO: Убедится, что все сценарии где Не определено в поле доставка блока Итого учтены



#
