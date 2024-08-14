"""В этом файле хранятся тесты для корзины"""
import time
import pytest
import allure
from playwright.sync_api import expect

from page_objects.cart_page import CartPage
from page_objects.autorization_modal_element import AutorizationModalElement
from page_objects.header_element import HeaderElement


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
    cart_page.activate_valid_promo_code()
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

# @pytest.mark.skip("Архив")
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
    cart_page.activate_valid_promo_code()
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
    cart_page.activate_valid_promo_code()
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


@allure.title("Применение валидного промокода")
def test_cart_aplying_a_valid_promo_code(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    assert cart_page.text_discount_budget() == "-5%"
    assert cart_page.discounted_price() == round(cart_page.base_price() * 0.95, 1)


@allure.title("Применение невалидного промокода")
def test_cart_aplying_a_invalid_promo_code(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    pre_action_price = cart_page.order_total_price()
    cart_page.activate_invalid_promo_code()
    post_action_price = cart_page.order_total_price()
    assert pre_action_price == post_action_price
    expect(cart_page.discount_budget()).not_to_be_visible()
    expect(cart_page.promo_code_field_info()).to_have_text("Промокод не действителен")


@allure.title("Раскрытие блока 'Промокод'")
def test_opening_promo_code_block(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    promo_code_bar_status = cart_page.promo_code_bar()
    expect(promo_code_bar_status).to_have_class('CartPromo__ToggleButton active')
    cart_page.close_promo_code_bar()
    expect(promo_code_bar_status).not_to_have_class('CartPromo__ToggleButton active')


@allure.title("Применение валидного промокода к неподходящему товару")
def test_cart_aplying_a_valid_promo_code_on_not_stm_product(page, base_url):
    cart_page = CartPage(page)
    # Добавить привлеченный товар и назвать функцию add_to_cart_not_stm_product
    cart_page.add_to_cart_not_stm_product(base_url)
    cart_page.open(base_url)
    cart_page.activate_valid_promo_code()
    # проверить, что скидки не появилось
    expect(cart_page.discount_budget()).not_to_be_visible()
    # проверить, что отобразилась нужная ошибка
    expect(cart_page.promo_code_field_info()).to_have_text("В корзине нет товаров, к которым можно применить введенный промокод")


@allure.title("Отмена промокода")
def test_canceling_promo_code(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    pre_action_price = cart_page.order_total_price()
    cart_page.activate_valid_promo_code()
    # отменить промокод
    cart_page.cancel_promo_code()
    post_action_price = cart_page.order_total_price()
    assert pre_action_price == post_action_price
    # убедится что скидки нет
    expect(cart_page.discount_budget()).not_to_be_visible()
    # убедится, что поле очищено
    expect(cart_page.promo_code_field()).to_have_attribute("data-empty", "true")


@allure.title("Очистка поля 'Промокод'")
def test_cleaning_intput_promo_code(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    cart_page.fill_valid_promo_code()
    # нажать крестик
    cart_page.clear_promo_code_field_by_cross()
    # убедится, что поле очищено
    expect(cart_page.promo_code_field()).to_have_attribute("data-empty", "true")

@allure.title("Активация подсказки")
def test_activating_a_hint(page, base_url):
    cart_page = CartPage(page)
    cart_page.add_to_cart_not_discounted_product(base_url)
    cart_page.open(base_url)
    cart_page.open_promo_code_bar()
    # Навести на i
    cart_page.hover_to_promo_code_hint()
    # Проверить поп-ап на присутствие
    expect(cart_page.promo_code_hint_popup()).to_be_visible()
    # сравнить тест с шаблоном (опцианально)
    assert cart_page.promo_code_hint_popup_text() == "Промокод действует на отдельные товары и в ограниченный период времени. Подробные условия действия промокода вы можете узнать в описании акции, при получении промокода или у наших специалистов."


"""Окно изменения цены"""


@allure.title("Удаление товара нажатием на крестик")
def test_delete_product_by_cross_on_changed_list(page, base_url):
    cart_page = CartPage(page)
    cart_page.info_change_block_activation(page, base_url)
    # Забрать наименование до удаления
    product_name_cart_list = cart_page.save_name_product_in_cart_list()
    product_name_change_info_list = cart_page.save_name_product_in_change_info_list()
    # Удалить
    cart_page.click_cross_button_delete_in_changed_list()
    # Забрать наименование после удаления
    expect(page.get_by_text(product_name_cart_list)).not_to_be_visible()
    expect(page.get_by_text(product_name_change_info_list)).not_to_be_visible()
    # Модальное коно осталось
    expect(cart_page.change_info_modal).to_be_visible()
    # проверить,что товар пропал из окна изменения информации? ДЛя этого там тоже нужну забрать и запомнить наименование


@allure.title("Вернутся в корзину через кнопку 'Вернутся в корзину'")
def test_(page, base_url):
    cart_page = CartPage(page)
    cart_page.info_change_block_activation(page, base_url)
    # нажать на вернутся в корзину
    cart_page.click_back_to_cart_button()
    # проверяем, что модалка закрыта
    expect(cart_page.change_info_modal).not_to_be_visible()
    expect(page).to_have_url(f"{base_url}/cart")


@allure.title("Вернутся в корзину через нажатие на пространство вне окна")
def test_(page, base_url):
    cart_page = CartPage(page)
    cart_page.info_change_block_activation(page, base_url)
    # нажать на пространство вне
    page.mouse.click(0, 0)
    # проверить, что вернулись в корзину, окно закрыто
    # проверяем, что модалка закрыта
    expect(cart_page.change_info_modal).not_to_be_visible()
    expect(page).to_have_url(f"{base_url}/cart")


"""Блок 'Недоступно для заказа'"""


@allure.title("Активация блока 'Недоступно для заказа'")
def test_not_available_for_order_block_activation(page, base_url):
    cart_page = CartPage(page)
    header = HeaderElement(page)
    cart_page.add_to_cart_multiple_stop_order_products(base_url)
    cart_page.open(base_url)
    header.change_location("Вахрушево")
    expect(cart_page.not_available_for_order_block).to_be_visible()

#доделать
@allure.title("Удаление товара нажатием на крестик")
def test_delete_product_by_cross_in_not_available_for_order_block(page, base_url):
    cart_page = CartPage(page)
    cart_page.not_available_for_order_block_activation(page, base_url)
    # Забрать наименование до удаления
    product_name = cart_page.save_name_product_in_not_availeble_list()
    # Удалить
    cart_page.click_cross_button_delete_in_not_availeble_list()
    # Забрать наименование после удаления
    expect(page.get_by_text(product_name)).not_to_be_visible()


@allure.title("Удаление всего товара в блоке")
def test_delete_all_products_in_not_available_for_order_block(page, base_url):
    cart_page = CartPage(page)
    cart_page.not_available_for_order_block_activation(page, base_url)
    # Удалить
    cart_page.click_head_not_availavle_delete_button()
    expect(cart_page.not_available_for_order_block).not_to_be_visible()












