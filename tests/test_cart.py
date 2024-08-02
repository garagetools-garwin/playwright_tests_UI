"""В этом файле хранятся тесты для корзины"""
import time
import pytest
import allure
from playwright.sync_api import expect

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
@pytest.mark.skip("Архив")
@pytest.mark.smoke
@allure.title("Открытие модального окна авторизации")
def test_cart_autorization_modal(page, base_url):
    cart_page = CartPage(page)
    autorization = AutorizationModalElement(page)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_order_button()
    expect(autorization.autorization_modal).to_be_visible()

@pytest.mark.skip("Архив")
@pytest.mark.smoke
@allure.title("Переход в чек-аут")
def test_cart_checkout(page, base_url):
    cart_page = CartPage(page)
    autorization = AutorizationModalElement(page)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    cart_page.click_order_button()
    autorization.cart_autorization_send_code()
    code = autorization.get_autorization_code_mail_ru()
    autorization.complete_autorization(code)
    # cart_page.click_to_checkbox_for_all_products() # При переходе в корзину, галочки сняты, проверить не баг ли это
    cart_page.click_order_button()
    expect(page).to_have_url(f"{base_url}/checkout")

@pytest.mark.skip("Архив")
@pytest.mark.smoke
@allure.title("Активация блока изменения информации")
def test_cart_info_change_block_activation(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_promocode()
    expect(cart_page.change_info_block).to_be_visible()

@pytest.mark.skip("Архив")
@allure.title("Выделение всего товара")
def test_cart_checkbox_for_all_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.all_checkbox_to_be_checked()
    cart_page.click_to_checkbox_for_all_products()
    cart_page.all_checkbox_not_to_be_checked()
@pytest.mark.skip("Архив")
@allure.title("Выделение части товара")
def test_cart_checkbox_for_multiple_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.click_first_checkbox_product()
    cart_page.first_checkbox_to_be_checked()
    cart_page.click_second_checkbox_product()
    cart_page.second_checkbox_to_be_checked()


"""!!!Второй блок тестов!!!"""

@pytest.mark.skip("Архив")
@allure.title("Число рядом с кнопкой удалить")
def test_delete_button_number(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.click_first_checkbox_product()
    cart_page.click_second_checkbox_product()
    cart_page.number_on_the_button_is_correct()

@pytest.mark.skip("Архив")
@allure.title("Удаление товара нажатием на кнопку 'Удалить'")
def test_delete_multiple_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.click_first_checkbox_product()
    cart_page.click_second_checkbox_product()
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.product_removed_from_cart()

@pytest.mark.skip("Архив")
@allure.title("Удаление товара нажатием на крестик")
def test_delete_product_by_cross(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.delete_product_by_cross()


"""Тесты для блока калькуляции"""

@pytest.mark.skip("Архив")
@allure.title("Изменение цены в блоке калькуляции по всем позициям")
def test_calculation_block_calculate_price_for_all_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    total_price = cart_page.calculate_total_price()
    cart_page.get_cart_prices()
    cart_page.compare_prices(total_price)

@pytest.mark.skip("Архив")
@allure.title("Изменение цены в блоке калькуляции по части позиций (Чек-бокс)")
def test_calculation_block_calculate_price_of_some_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.order_price_is_zero()
    cart_page.click_first_checkbox_product()
    cart_page.calculate_total_price_for_checked_products()
    cart_page.click_second_checkbox_product()
    cart_page.calculate_total_price_for_checked_products()

@pytest.mark.skip("Архив")
@allure.title("Активация окна изменения цены")
def test_cart_info_change_modal_activation(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_promocode()
    cart_page.click_details_button()
    expect(cart_page.change_info_modal).to_be_visible()

@pytest.mark.skip("Архив")
@allure.title("Отправка на печать")
def test_cart_print_form_activation(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    page.evaluate("(() => {window.waitForPrintDialog = new Promise(f => window.print = f);})()")
    cart_page.click_print_button()
    page.wait_for_function("window.waitForPrintDialog")

@pytest.mark.skip("Архив")
@allure.title("Изменение количества товара через счетчик")
def test_cart_counter(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    quantity = cart_page.get_quantity_of_product()
    assert quantity[0] == 1
    page.locator("button:nth-child(3)").first.click()
    quantity = cart_page.get_quantity_of_product()
    assert quantity[0] == 2
    page.locator(".Counter__Element").first.click()
    quantity = cart_page.get_quantity_of_product()
    assert quantity[0] == 1


@pytest.mark.skip("Архив")
@allure.title("Изменение цены в блоке калькуляции по части позиций (Счетчик)")
def test_cart_calculation_block_calculate_price_of_some_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart(base_url)
    cart_page.open(base_url)
    price_text = page.locator('.AvailableList.CartPage__AvailableProductList .Price__Value').nth(0).inner_text()
    price = int(price_text.replace('\xa0', '').replace(' ', ''))
    print(price)
    total_price = cart_page.order_total_price()
    print(total_price)
    assert price == total_price
    # взять цену перваой позиции - first_product_price
    # total_price = cart_page.calculate_total_price()
    # cart_page.compare_prices()
    # сравнить цену прервой позиции с суммой в блоке калькуляции
    page.locator("button:nth-child(3)").first.click()  #первый плюс
    new_price = price+price
    print(new_price)
    total_price = cart_page.order_total_price()
    print(total_price)
    assert new_price == total_price
    #  new_first_product_price = first_product_price *2
    # взять сумму блока калькуляции
    # new_first_product_price ==  с суммой в блоке калькуляции
    page.locator(".Counter__Element").first.click()  # первый плюс
    old_price = new_price-price
    total_price = cart_page.order_total_price()
    assert old_price == total_price
    # взять цену перваой позиции
    # взять сумму блока калькуляции
    # сравнить цену прервой позиции с суммой в блоке калькуляции



"""3 блок"""


@allure.title("Закрытие блока изменения информации")
def test_cart_info_change_block_close(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_promocode()
    cart_page.click_ok_button()
    expect(cart_page.change_info_block).not_to_be_visible()


@allure.title("Удаление всего товара")
def test_cart_deletion_all_products(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.cart_is_empty()


@allure.title("Отмена удаления товара")
def test_cart_cancel_deletion(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.cancel_deletion()
    cart_page.deletion_modal_not_visible()


@allure.title("Переход с пустой корзины 'На главную'")
def test_cart_move_from_cart_to_home(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.click_home_button()
    expect(page).to_have_url(f"{base_url}/")

@allure.title("Активация окна авторизации в пустой корзине")
def test_cart_activation_authorization_modal_frome_empty_cart(page, base_url):
    cart_page = CartPage(page)
    autorization = AutorizationModalElement(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_head_delete_button()
    cart_page.confirm_deletion()
    cart_page.click_autorization_button()
    expect(autorization.autorization_modal).to_be_visible()

@allure.title("Если товар не выбран кнопка 'Оформить заказ' не активна")
def test_test_order_button_is_blocked(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_multiple_products(base_url)
    cart_page.open(base_url)
    cart_page.click_to_checkbox_for_all_products()
    cart_page.order_button_is_disabled()


"""Промокод"""

@allure.title("Закрытие блока изменения информации")
def test_cart_info_change_block_close(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_promocode()
    cart_page.click_ok_button()
    expect(cart_page.change_info_block).not_to_be_visible()





