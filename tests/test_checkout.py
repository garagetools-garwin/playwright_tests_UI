"""В этом файле хранятся тесты для чекаут"""
import time

import pytest
import allure

from playwright.sync_api import expect
from page_objects.checkout_page import CheckoutPage
from page_objects.cart_page import CartPage


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
    with allure.step("Запоминаю сумму заказа"):
        total_price = cart_page.order_total_price()
    with allure.step("Проверяю, что стоимость двух товаров равняется сумме заказа"):
        assert new_price == total_price
    with allure.step("Уменьшаю количество товара на 1"):
        page_fixture.locator(".Counter__Element").nth(0).click()  # первый плюс
    with allure.step("Проверяю, что сумма заказа равна сумме одной единице товара"):
        total_price = cart_page.order_total_price()
        assert price == total_price

        """Блок Покупатель и получатель"""


@pytest.mark.auth
@allure.title("Добавление нового получателя со всеми полями")
def test_add_new_recipient_with_all_fields(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.add_recipient_modal.add_recipient()
    name, phone, email = checkout_page.add_recipient_modal.fill_in_data_randomize()
    checkout_page.add_recipient_modal.save_new_recipient()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing()

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = f"{email}, {phone}"
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)


@pytest.mark.auth
@allure.title("Добавление нового получателя только с обязательными полями")
def test_add_new_recipient_with_part_of_the_fields(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.add_recipient_modal.add_recipient()
    name, phone = checkout_page.add_recipient_modal.fill_in_part_of_data_randomize()
    checkout_page.add_recipient_modal.save_new_recipient()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing()

    with allure.step("Формирую ожидаемый текст"):
        expected_info_title = name
        expected_info_description = phone
    with allure.step("Проверяю информацию о выбранном получателе"):
        checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title, expected_info_description)


@pytest.mark.auth
@allure.title("Создание нового получателя со всеми валидными символами в ФИО")
def test_add_new_recipient_with_name_with_all_valid_simbols(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.add_recipient_modal.add_recipient()
    with allure.step("Ввожу текст в котором включены все допустимые буквы и символы, их максимальное количество"):
        name, phone, email = checkout_page.add_recipient_modal.fill_in_data()
    checkout_page.add_recipient_modal.save_new_recipient()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing()

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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.add_recipient_modal.add_recipient()
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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.add_recipient_modal.add_recipient()
    checkout_page.add_recipient_modal.close_new_recipient_modal2()


"""Листинг получателей"""


@pytest.mark.auth
@allure.title("Выбор нового получателя")
def test_select_a_new_recipient(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
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
    checkout_page.recipient_listing.open_recipient_listing()
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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_delete_button()


"""Модальное окно подтверждения удаления"""


@pytest.mark.auth
@allure.title("Удаление получателя")
def test_deletion_recipient(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.delete_conformation_modal.delete_recipient()


@pytest.mark.auth
@allure.title("Отмена удаления получателя")
def test_cancel_recipient_deletion(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.delete_conformation_modal.cancel_recipient_deletion()


@pytest.mark.auth
@allure.title("Закрытие окна удаления получателя")
def test_close_recipient_deletion_modal(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.delete_conformation_modal.close_recipient_deletion_modal()


"""Модальное окно Изменить получателя"""


@pytest.mark.auth
@allure.title("Открытие окна Изменить получателя")
def test_close_recipient_deletion_modal(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.recipient_listing.open_recipient_listing()
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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    name, phone, email = checkout_page.edit_recipient_modal.fill_in_data_randomize()
    checkout_page.edit_recipient_modal.save_edited_recipient()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing()

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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    name, phone = checkout_page.edit_recipient_modal.fill_in_part_of_data_randomize()
    email = checkout_page.edit_recipient_modal.save_email()
    checkout_page.edit_recipient_modal.save_edited_recipient()
    with allure.step("Формирую ожидаемый текст"):
        # Если имейла нет, формируем ожидаемый результат без него
        if email:
            expected_info = f"{name}, {email}, {phone}"
        else:
            expected_info = f"{name}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing()

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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    with allure.step("Ввожу текст в котором включены все допустимые буквы и символы, их максимальное количество"):
        name, phone, email = checkout_page.edit_recipient_modal.fill_in_data()
    checkout_page.edit_recipient_modal.save_edited_recipient()
    with allure.step("Формирую ожидаемый текст"):
        expected_info = f"{name}, {email}, {phone}"
    checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
    checkout_page.recipient_listing.open_recipient_listing()

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
    checkout_page.recipient_listing.open_recipient_listing()
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
    checkout_page.recipient_listing.open_recipient_listing()
    checkout_page.recipient_listing.open_action_menu()
    checkout_page.recipient_listing.click_edit_button()
    checkout_page.edit_recipient_modal.close_edit_recipient_modal2()


"""Блок Получение"""

@pytest.mark.auth
@allure.title("Открытие листинга адресов пользователем с адресами")
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
    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.click_add_adress_button()
    with allure.step("Провряю, что карты отображается на странице"):
        expect(checkout_page.map.map_modal()).to_be_visible()


@pytest.mark.auth
@allure.title("Добавление ПВЗ")
def test_pickup_point_adding(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.click_add_adress_button()

    with allure.step("Проверяю, что кнопка Пункт выдачи предвыбрана"):
        expect(checkout_page.map.pickup_point_button_status()).to_have_class('CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')

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

    with allure.step("Запоминаю адрес ПВЗ в блоке Получение"):
        obtaining_block_adress = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Проверяю, что в блоке Получения установлися адресс выбранного ПВЗ"):
        assert map_modal_adress == obtaining_block_adress

    checkout_page.obtaining_block.adress_listing_activation()

    checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)

    with allure.step("Удаляю запись"):
        checkout_page.adress_listing.open_action_menu()
        checkout_page.delete_conformation_modal.delete_adress()


@pytest.mark.auth
@allure.title("Редактирование ПВЗ")
def test_pickup_point_editing(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)

    with allure.step("Создаю новый адрес"):
        checkout_page.obtaining_block.adress_listing_activation()
        checkout_page.adress_listing.click_add_adress_button()

        # Выбор ПВЗ с кастомным событием
        pickup_point_id = "75048c93-dfb2-422d-b17b-ff95ad2193c8"
        target_lat = 59.88164
        target_lon = 30.273926
        checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)
        checkout_page.map.click_pick_up_here_button()

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

        checkout_page.obtaining_block.adress_listing_activation()

        checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)

        with allure.step("Удаляю запись"):
            checkout_page.adress_listing.open_action_menu()
            checkout_page.delete_conformation_modal.delete_adress()

#TODO: долделать два теста ниже
@pytest.mark.auth
@allure.title("Добавление адреса курьера")
def test_courier_adress_adding(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.click_add_adress_button()
    checkout_page.map.click_courier_button()

    with allure.step("Проверяю, что появилось поле Адрес"):
        expect(checkout_page.map.adress_textaria_status()).to_be_visible()

    with allure.step("Ввожу адрес в поле Адрес"):
        checkout_page.map.type_in_textaria("г Санкт-Петербург, ул Ленина, д 31")

    with allure.step("Запоминаю адрес ПВЗ в модальном окне Карты"):
        map_modal_adress = checkout_page.map.text_from_first_adress_in_list().inner_text()

    checkout_page.map.click_first_adress_in_list()
    checkout_page.map.click_pick_up_here_button()

    with allure.step("Запоминаю адрес ПВЗ в блоке Получение"):
        obtaining_block_adress = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Проверяю, что в блоке Получения установлися адресс выбранного ПВЗ"):
        assert map_modal_adress == obtaining_block_adress

    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)

    with allure.step("Удаляю запись"):
        checkout_page.adress_listing.open_action_menu()
        checkout_page.delete_conformation_modal.delete_adress()

@pytest.mark.auth
@allure.title("Редактирование адреса курьера")
def test_courier_adress_editing(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)

    with allure.step("Создаю новый адрес"):
        checkout_page.obtaining_block.adress_listing_activation()
        checkout_page.adress_listing.click_add_adress_button()
        checkout_page.map.click_courier_button()

        with allure.step("Ввожу адрес в поле Адрес"):
            checkout_page.map.type_in_textaria("Санкт-Петербург, Невский проспект, 64")

        checkout_page.map.click_first_adress_in_list()
        checkout_page.map.click_pick_up_here_button()

        with allure.step("Запоминаю адрес ПВЗ в блоке Получение"):
            obtaining_block_adress_first = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Редактирую адрес"):
        checkout_page.obtaining_block.courier_adress_listing_activation()
        checkout_page.adress_listing.open_action_menu()
        checkout_page.adress_listing.click_edit_button()
        checkout_page.map.type_in_textaria("г Санкт-Петербург, ул Ленина, д 31")

        with allure.step("Запоминаю адрес ПВЗ в модальном окне Карты"):
            map_modal_adress = checkout_page.map.text_from_first_adress_in_list().inner_text()

        checkout_page.map.click_first_adress_in_list()
        checkout_page.map.click_pick_up_here_button()

    with allure.step("Запоминаю адрес ПВЗ в блоке Получение"):
        obtaining_block_adress_second = checkout_page.obtaining_block.pickup_point_adress().inner_text()

    with allure.step("Проверяю, что в блоке Получения установлися адресс выбранного ПВЗ"):
        assert map_modal_adress == obtaining_block_adress_second

    with allure.step("Проверяю, что новый адрес отличается от предыдушего"):
        assert obtaining_block_adress_first != obtaining_block_adress_second

    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.verify_selected_adress_info(map_modal_adress)

    with allure.step("Удаляю запись"):
        checkout_page.adress_listing.open_action_menu()
        checkout_page.delete_conformation_modal.delete_adress()

@pytest.mark.auth
@allure.title("Активация окна Удалить адрес")
def test_activate_delete_confirmation_modal_obtaining(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.open_action_menu()
    checkout_page.adress_listing.click_delete_button()


@pytest.mark.auth
@allure.title("Удаление адреса")
def test_deletion_adress(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation()
    checkout_page.adress_listing.open_action_menu()
    checkout_page.delete_conformation_modal.delete_adress()


@pytest.mark.auth
@allure.title("Выбор нового адреса")
def test_select_a_new_recipient(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.adress_listing_activation()
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
        expect(checkout_page.map.courier_button_status()).to_have_class('CheckoutChooseMethod__Button Button size--small color--secondary --is-selected')

@pytest.mark.auth
@allure.title("Откработка кнопки Назад")
def test_back_button(page_fixture, base_url):
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    cart_page.open(base_url)
    cart_page.clear_cart()
    cart_page.add_to_cart(base_url)
    checkout_page.open(base_url)
    checkout_page.obtaining_block.pickup_point_adress_listing_activation()

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



#TODO: сделать удаление получателя после создания
#TODO: Перед изменение получателя и адреса всегда создавать нового получателя и удалять его
#TODO: После изменения создания и удаление получателя адреса проверять их title и description
#TODO: рассмотреть вариант при изменении адреса менять его на GDP и наоборот

