"""В этом файле хранятся тесты для корзины"""
import time
import pytest
import allure
from playwright.sync_api import expect

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.header_element import HeaderElement


@pytest.mark.smoke
@pytest.mark.testit_case_title("Проверка первой успешной загрузки файла")
@allure.title("Открытие модального окна авторизации")
def test_cart_autorization_modal(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    autorization = AutorizationModalElement(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_order_button()
    with allure.step("Проверяю, что окно аторизаци отображается на странице"):
        expect(autorization.autorization_modal).to_be_visible()


@pytest.mark.smoke
@pytest.mark.skip("Временно, пока не напишу новый метод на авторизацию")
@allure.title("Переход в чек-аут")
def test_cart_checkout(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    autorization = AutorizationModalElement(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_order_button()
    autorization.cart_autorization_send_code()
    code = autorization.get_autorization_code_mail_ru()
    autorization.complete_autorization(code)
    # cart_page.click_to_checkbox_for_all_products() # При переходе в корзину, галочки сняты, проверить не баг ли это
    cart_page.click_order_button()
    with allure.step("Проверяю, что пользователь перешел в чек-аут"):
        expect(page_fixture).to_have_url(f"{base_url}/checkout")


@pytest.mark.smoke
@allure.title("Активация блока изменения информации")
def test_cart_info_change_block_activation(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    with allure.step("Проверяю, что блок изменения информации отображается на странице"):
        expect(cart_page.change_info_block).to_be_visible()


@allure.title("Выделение всего товара")
def test_cart_checkbox_for_all_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.all_checkbox_to_be_checked()
    cart_page.click_to_checkbox_for_all_products()
    cart_page.all_checkbox_not_to_be_checked()

@allure.title("Выделение части товара")
def test_cart_checkbox_for_multiple_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.click_first_checkbox_product()
    cart_page.first_checkbox_to_be_checked()
    cart_page.click_second_checkbox_product()
    cart_page.second_checkbox_to_be_checked()


"""!!!Второй блок тестов!!!"""


@allure.title("Число рядом с кнопкой удалить")
def test_delete_button_number(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.click_first_checkbox_product()
    cart_page.click_second_checkbox_product()
    cart_page.number_on_the_button_is_correct()


@allure.title("Удаление товара нажатием на кнопку 'Удалить'")
def test_delete_multiple_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.click_first_checkbox_product()
    cart_page.click_second_checkbox_product()
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.product_removed_from_cart()


@allure.title("Удаление товара нажатием на крестик (Корзина)")
def test_delete_product_by_cross(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.delete_product_by_cross()


"""Тесты для блока калькуляции"""


@allure.title("Изменение цены в блоке калькуляции по всем позициям")
def test_calculation_block_calculate_price_for_all_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    total_price = cart_page.calculate_total_price()
    cart_page.get_cart_prices()
    cart_page.compare_prices(total_price)


@allure.title("Изменение цены в блоке калькуляции по части позиций (Чек-бокс)")
def test_calculation_block_calculate_price_of_some_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.order_price_is_zero()
    cart_page.click_first_checkbox_product()
    cart_page.calculate_total_price_for_checked_products()
    cart_page.click_second_checkbox_product()
    cart_page.calculate_total_price_for_checked_products()


@allure.title("Активация окна изменения цены")
def test_cart_info_change_modal_activation(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    cart_page.click_details_button()
    with allure.step("Проверяю, что окно изменения информации отображается на странице"):
        expect(cart_page.change_info_modal).to_be_visible()


@allure.title("Отправка на печать")
def test_cart_print_form_activation(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_print_button()
    with allure.step("Проверяю, что окно печати на странице"):
        page_fixture.wait_for_function("window.waitForPrintDialog")


@allure.title("Изменение количества товара через счетчик")
def test_cart_counter(page_fixture, base_url):
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
def test_cart_calculation_block_calculate_price_of_some_products(page_fixture, base_url):
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


"""3 блок"""


@allure.title("Закрытие блока изменения информации")
def test_cart_info_change_block_close(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    cart_page.click_ok_button()
    with allure.step("Проверяю, что блок изменения информации больше не отображается на странице"):
        expect(cart_page.change_info_block).not_to_be_visible()


@allure.title("Удаление всего товара (Корзина)")
def test_cart_deletion_all_products(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.cart_is_empty()


@allure.title("Отмена удаления товара")
def test_cart_cancel_deletion(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.cancel_deletion()
    cart_page.deletion_modal_not_visible()


@allure.title("Переход с пустой корзины 'На главную'")
def test_cart_move_from_cart_to_home(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.click_home_button()
    with allure.step("Проверяю, что пользователь находится на главной странице"):
        expect(page_fixture).to_have_url(f"{base_url}/")


@allure.title("Активация окна авторизации в пустой корзине")
def test_cart_activation_authorization_modal_frome_empty_cart(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    autorization = AutorizationModalElement(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.click_autorization_button()
    with allure.step("Проверяю, что окно авторизации отоброажается на странице"):
        expect(autorization.autorization_modal).to_be_visible()


@allure.title("Если товар не выбран кнопка 'Оформить заказ' не активна")
def test_test_order_button_is_blocked(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.order_button_is_disabled()


"""Промокод"""


@allure.title("Применение валидного промокода")
def test_cart_aplying_a_valid_promo_code(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    with allure.step("Проверяю, что скидка на плашке равна 5%"):
        assert cart_page.text_discount_budget() == "-5%"
    with allure.step("Проверяю, что цена товара равна его первоначальной стоимости - 5%"):
        assert cart_page.discounted_price() == round(cart_page.base_price() * 0.95, 1)


@allure.title("Применение невалидного промокода")
def test_cart_aplying_a_invalid_promo_code(page_fixture, base_url):
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
def test_opening_promo_code_block(page_fixture, base_url):
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
def test_cart_aplying_a_valid_promo_code_on_not_stm_product(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_stm_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    with allure.step("Проверяю, что плашка со скидкой не отображается"):
        expect(cart_page.discount_budget()).not_to_be_visible()
    with allure.step("Проверяю, что на странице отображается подсказка 'В корзине нет товаров, к которым можно применить введенный промокод'"):
        expect(cart_page.promo_code_field_info()).to_have_text("В корзине нет товаров, к которым можно применить введенный промокод")


@allure.title("Отмена промокода")
def test_canceling_promo_code(page_fixture, base_url):
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
def test_cleaning_intput_promo_code(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    cart_page.fill_valid_promo_code()
    cart_page.clear_promo_code_field_by_cross()
    with allure.step("Проверяю, что поле 'Промокод' - пустое"):
        expect(cart_page.promo_code_field()).to_have_attribute("data-empty", "true")

@allure.title("Активация подсказки")
def test_activating_a_hint(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    cart_page.hover_to_promo_code_hint()
    with allure.step("Проверяю, что подсказка отображается на странице"):
        expect(cart_page.promo_code_hint_popup()).to_be_visible()
    with allure.step("Проверяю, что текст подсказки соответствует шаблону"):
        assert cart_page.promo_code_hint_popup_text() == "Промокод действует на отдельные товары и в ограниченный период времени. Подробные условия действия промокода вы можете узнать в описании акции, при получении промокода или у наших специалистов."


"""Окно изменения цены"""


@allure.title("Удаление товара нажатием на крестик (Окно изменения цены)")
def test_delete_product_by_cross_on_changed_list(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.info_change_block_activation(page_fixture, base_url)
    with allure.step("Запоминаю название товара в корзине"):
        product_name_cart_list = cart_page.save_name_product_in_cart_list()
    with allure.step("Запоминаю название товара в списке окна изменения цены"):
        product_name_change_info_list = cart_page.save_name_product_in_change_info_list()
    cart_page.click_cross_button_delete_in_changed_list()
    with allure.step("Проверяю, что товар больше не отображается в корзине"):
        expect(page_fixture.get_by_text(product_name_cart_list)).not_to_be_visible()
    with allure.step("Проверяю, что товар больше не отображается в списке окна изменения цены"):
        expect(page_fixture.get_by_text(product_name_change_info_list)).not_to_be_visible()
    with allure.step("Проверяю, что окно изменения цены осталось на странице"):
        expect(cart_page.change_info_modal).to_be_visible()


@allure.title("Вернутся в корзину через кнопку 'Вернутся в корзину'")
def test_back_to_cart_from_modal_1(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.info_change_block_activation(page_fixture, base_url)
    cart_page.click_back_to_cart_button()
    with allure.step("Проверяю, что окно изменения цены больше не отображается на странице"):
        expect(cart_page.change_info_modal).not_to_be_visible()
    with allure.step("Проверяю, что пользователь находится в корзине"):
        expect(page_fixture).to_have_url(f"{base_url}/cart")


@allure.title("Вернутся в корзину через нажатие на пространство вне окна")
def test_back_to_cart_from_modal_2(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.info_change_block_activation(page_fixture, base_url)
    with allure.step("Нажимаю на пространство вне окна"):
        page_fixture.mouse.click(0, 0)
    with allure.step("Проверяю, что окно изменения цены больше не отображается на странице"):
        expect(cart_page.change_info_modal).not_to_be_visible()
    with allure.step("Проверяю, что пользователь находится в корзине"):
        expect(page_fixture).to_have_url(f"{base_url}/cart")


"""Блок 'Недоступно для заказа'"""


@allure.title("Активация блока 'Недоступно для заказа'")
def test_not_available_for_order_block_activation(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    header = HeaderElement(page_fixture)
    cart_page.add_to_cart_multiple_stop_order_products(base_url)
    cart_page.open(base_url)
    header.change_location("Вахрушево")
    with allure.step("Проверяю, что блок 'Недоступно для заказа' отображается на странице"):
        expect(cart_page.not_available_for_order_block).to_be_visible()

@allure.title("Удаление товара нажатием на крестик (Блок 'Недоступно для заказа')")
def test_delete_product_by_cross_in_not_available_for_order_block(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.not_available_for_order_block_activation(page_fixture, base_url)
    with allure.step("Запоминаю название товара до удаления"):
        product_name = cart_page.save_name_product_in_not_availeble_list()
    cart_page.click_cross_button_delete_in_not_availeble_list()
    with allure.step("Проверяю, что товар больше не отображается"):
        expect(page_fixture.get_by_text(product_name)).not_to_be_visible()

@allure.title("Удаление всего товара в блоке (Блок 'Недоступно для заказа')")
def test_delete_all_products_in_not_available_for_order_block(page_fixture, base_url):
    cart_page = CartPage(page_fixture)
    cart_page.not_available_for_order_block_activation(page_fixture, base_url)
    cart_page.click_head_not_availavle_delete_button()
    with allure.step("Проверяю, что блок 'Недоступно для заказа' больше не отображается"):
        expect(cart_page.not_available_for_order_block).not_to_be_visible()












