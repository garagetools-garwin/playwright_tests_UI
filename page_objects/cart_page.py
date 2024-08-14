import random
import playwright
from bs4 import BeautifulSoup
from playwright.sync_api import Error
from playwright.sync_api import TimeoutError

import pytest
from playwright.sync_api import expect

from page_objects.header_element import HeaderElement


class CartPage:

    PATH = "/cart"
    ORDER_BUTTON = ".OrderTotal__Button.Button.size--medium.color--primary"
    CHANGE_INFO_BLOCK = ".flexRow-JCSB-AIC.InfoBlock.CartChangeInfoBlock"
    CHECKBOX_HEAD = ".flexRow-JCSB-AIC.CartAvailableListHead .Checkbox__Button"
    CHECKBOX_PRODUCT = ".AvailableList.CartPage__AvailableProductList .Checkbox__Button"
    AVAILABLE_PRODUCT_LIST = ".AvailableList.CartPage__AvailableProductList"
    PRODUCT_ROW = ".flexRow-JCSB-AIC.CartAvailableListRow"
    HEAD_DELETE_BUTTON = ".flexRow-AIC.CartAvailableListHead__RemoveBtn"
    HEAD_DELETE_BUTTON_TEXT = "button.flexRow-AIC.CartAvailableListHead__RemoveBtn span"
    NOT_AVAILABLE_HEAD_DELETE_BUTTON = ".flexRow-AIC.CartUnavailableListHead__DeleteButton"
    CART_LIST_ROW_DELETE_BUTTON = ".CartAvailableListRow__RemoveBtn"
    CART_CHANGET_LIST_ROW_DELETE_BUTTON = ".CartChangedListRow__RemoveBtn"
    NOT_AVAILABLE_LIST_ROW_DELETE_BUTTON = ".CartUnavailableListRow__RemoveBtn"
    CONFIRM_DELETE_BUTTON = ".Button.size--big.color--primary"
    CANCEL_DELETE_BUTTON = ".Button.size--big.color--tertiary"
    ORDER_TOTAL_PRICE = ".flexRow-AIFE.Price.OrderTotal__Price .Price__Value"
    DETALES_BUTTON = ".CartChangeInfoBlock__Actions__Element.Button.size--normal.color--tertiary"
    OK_BUTTON = ".CartChangeInfoBlock__Actions__Element.Button.size--normal.color--secondary"
    CHANGE_INF0_MODAL = ".flexColumn.KitModal__Inner"
    DELETION_MODAL = ".flexColumn.KitModal__Inner"
    PRINT_BUTTON = ".CartAvailableListHead__PrintBtn.flexRow-AIC"
    HOME_BUTTON = ".EmptyBlock__MainButton.nuxt-link-active.Button.flexRow.size--normal.color--tertiary"
    CART_IS_EMPTY = ".EmptyBlock__Title"
    AUTORIZATION_BUTTON = ".EmptyBlock__LoginButton.Button.size--normal.color--primary"
    DISCOUNT_BUDGET = ".ProductCartPricing.flexColumn.ProductCart__Pricing .PricingBadge"
    PRODUCT_PRICE_BASE = ".flexRow-AIFE.Price.ProductCartPricing__Base"
    PRODUCT_PRICE_DISCOUNTED = ".flexRow-AIFE.Price.ProductCartPricing__User"
    PROMO_CODE_FIELD_INFO = ".Field.CartPromo__Field .Field__Info .Field__Text"
    CLEAR_PROMO_CODE_FIELD_BUTTON = ".flexRow-C.FieldControls__Button.active"
    PROMO_CODE_FIELD = ".Field.CartPromo__Field.is-small.has-controls"
    PROMO_CODE_HINT_ICON = ".flexRow-AIC.Tooltip.CartPromo__Tooltip"
    PROMO_CODE_HINT_POPUP = ".Tooltip__Inner.v-enter-to .Tooltip__Content"
    CANCEL_PROMO_CODE_BUTTON = ".flexRow-AIC.CartPromo__CancelButton"
    BACK_TO_CART_BUTTON = ".Button size--big.color--secondary"
    NOT_AVAILABLE_FOR_ORDER_BLOCK = "div.CartUnavailableList"




    def __init__(self, page):
        self.page = page
        self.change_info_block = page.locator(self.CHANGE_INFO_BLOCK)
        self.change_info_modal = page.locator(self.CHANGE_INF0_MODAL)
        self.not_available_for_order_block = page.locator(self.NOT_AVAILABLE_FOR_ORDER_BLOCK)
        self.checkbox_for_all_products = page.locator(self.CHECKBOX_HEAD).nth(0)

    def open(self, url):
        self.page.goto(url + self.PATH)

    def add_to_cart(self, url):
        urls_to_check = [
            f"{url}/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd",
            f"{url}/tovar/bita-udarnaya-1-4-ph1-25mm"
        ]

        for url in urls_to_check:
            self.page.goto(url)

            try:
                # Попытка найти и нажать кнопку "Добавить в корзину"
                self.page.get_by_text(" Добавить в корзину ").click()
                break  # Прерываем цикл, если кнопка найдена и товар добавлен
            except Exception:
                print(f"Add to cart button not found on {url}")
                continue  # Переходим к следующей ссылке, если кнопка не найдена
        else:
            raise ValueError("Product not available, please select another product")

    def click_order_button(self):
        self.page.locator(self.ORDER_BUTTON).click()

    def add_to_cart_multiple_products(self, base_url):
        urls_to_check = [
            f"{base_url}/tovar/bita-udarnaya-1-4-ph1-25mm",
            f"{base_url}/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd",
            f"{base_url}/tovar/klyuch-rozhkovyy-12h14mm1"
        ]

        for url in urls_to_check:
            self.page.goto(url)
            try:
                # Попытка найти и нажать кнопку "Добавить в корзину"
                self.page.locator("text=Добавить в корзину").click()
            except Exception as e:
                print(f"Add to cart button not found on {url}. Exception: {e}")
                continue  # Переходим к следующей ссылке, если кнопка не найдена

        # Проверка, если ни один товар не был добавлен в корзину
        if not any(self.page.url == url for url in urls_to_check):
            raise ValueError("Product not available, please select another product")

    def add_to_cart_multiple_stop_order_products(self, base_url):
        urls_to_check = [
            f"{base_url}/tovar/elektrody-dlya-kolets-8h16-o-16",
            f"{base_url}/tovar/polotno-po-metallu-bimetallicheskoe-305x13x0-65-mm-18t-m42",
            f"{base_url}/tovar/razreznoy-klyuch-7-16-x-1-2"
        ]

        for url in urls_to_check:
            self.page.goto(url)
            try:
                # Попытка найти и нажать кнопку "Добавить в корзину"
                self.page.locator("text=Добавить в корзину").click()
            except Exception as e:
                print(f"Add to cart button not found on {url}. Exception: {e}")
                continue  # Переходим к следующей ссылке, если кнопка не найдена

        # Проверка, если ни один товар не был добавлен в корзину
        if not any(self.page.url == url for url in urls_to_check):
            raise ValueError("Product not available, please select another product")

    def add_to_cart_not_stm_product(self, url):
        urls_to_check = [
            f"{url}/tovar/lom-oborochnyy-lo-3-0",
            f"{url}/tovar/nasos-drenazhnyy-pogruzhnoy-4-gnom-25-20"
        ]

        for url in urls_to_check:
            self.page.goto(url)

            try:
                # Попытка найти и нажать кнопку "Добавить в корзину"
                # assert self.page.locator("flexRow-AIFE Price.ProductCardControls__Pricing__BasePrice.is--discounted").is_visible()
                self.page.get_by_text(" Добавить в корзину ").click()
                break  # Прерываем цикл, если кнопка найдена и товар добавлен
            except Exception:
                print(f"Add to cart button not found on {url}")
                continue  # Переходим к следующей ссылке, если кнопка не найдена
        else:
            raise ValueError("Product not available, please select another product")

    def add_to_cart_not_discounted_product(self, url):
        urls_to_check = [
            f"{url}/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd",
            f"{url}/tovar/bita-udarnaya-1-4-ph1-25mm"
        ]

        for url in urls_to_check:
            self.page.goto(url)

            try:
                # Попытка найти и нажать кнопку "Добавить в корзину"
                # assert self.page.locator("flexRow-AIFE Price.ProductCardControls__Pricing__BasePrice.is--discounted").is_visible()
                self.page.get_by_text(" Добавить в корзину ").click()
                break  # Прерываем цикл, если кнопка найдена и товар добавлен
            except Exception:
                print(f"Add to cart button not found on {url}")
                continue  # Переходим к следующей ссылке, если кнопка не найдена
        else:
            raise ValueError("Product not available, please select another product")

    def open_promo_code_bar(self):
        self.page.locator(".CartPromo__ToggleButton").click()

    def promo_code_bar(self):
        return self.page.locator(".CartPromo__ToggleButton")

    def close_promo_code_bar(self):
        self.open_promo_code_bar()

    def fill_valid_promo_code(self):
        self.page.locator(".kit-input.Field__Input.disable-label").nth(1).fill("НАЧАЛО")

    def fill_invalid_promo_code(self):
        self.page.locator(".kit-input.Field__Input.disable-label").nth(1).fill("12345DF")

    def click_apply_button(self):
        self.page.locator("//*[text()='Применить']").click()

    def activate_valid_promo_code(self):
        self.open_promo_code_bar()
        self.fill_valid_promo_code()
        self.click_apply_button()

    def activate_invalid_promo_code(self):
        self.open_promo_code_bar()
        self.fill_invalid_promo_code()
        self.click_apply_button()

    def all_checkbox_to_be_checked(self):
        for i in range(self.page.locator(self.CHECKBOX_PRODUCT).count()):
            expect(self.page.locator(self.CHECKBOX_PRODUCT).nth(i)).to_be_checked()

    def all_checkbox_not_to_be_checked(self):
        for i in range(self.page.locator(self.CHECKBOX_PRODUCT).count()):
            expect(self.page.locator(self.CHECKBOX_PRODUCT).nth(i)).not_to_be_checked()

    def click_to_checkbox_for_all_products(self):
        self.checkbox_for_all_products.click()

    def click_first_checkbox_product(self):
        first = self.page.locator(self.CHECKBOX_PRODUCT).nth(1).click()
        expect(self.page.locator(self.CHECKBOX_PRODUCT).nth(1)).to_be_checked()

    def click_second_checkbox_product(self):
        self.page.locator(self.CHECKBOX_PRODUCT).nth(2).click()

    def first_checkbox_to_be_checked(self):
        expect(self.page.locator(self.CHECKBOX_PRODUCT).nth(1)).to_be_checked()

    def second_checkbox_to_be_checked(self):
        expect(self.page.locator(self.CHECKBOX_PRODUCT).nth(2)).to_be_checked()

    def count_all_checked_checkbox(self):
        checkboxes = self.page.locator(self.CHECKBOX_PRODUCT)
        count = 0
        for i in range(checkboxes.count()):
            if checkboxes.nth(i).is_checked():
                count += 1
        return count

    def text_discount_budget(self):
        text_discount_budget = self.page.locator(self.DISCOUNT_BUDGET).inner_text()
        return text_discount_budget

    def discounted_price(self):
        text_discounted_price = self.page.locator(self.PRODUCT_PRICE_DISCOUNTED).inner_text()
        discounted_price_number = float(text_discounted_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.'))
        return discounted_price_number

    def base_price(self):
        text_base_price = self.page.locator(self.PRODUCT_PRICE_BASE).inner_text()
        base_price_number = float(text_base_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.'))
        return base_price_number

    def discount_budget(self):
        discount_budget = self.page.locator(self.DISCOUNT_BUDGET)
        return discount_budget

    def text_delete_button(self):
        text_delete_button = self.page.locator(self.HEAD_DELETE_BUTTON_TEXT).inner_text()
        parts = text_delete_button.split()
        number_part = parts[1]
        number_in_btn_text = int(number_part.strip("()"))
        return number_in_btn_text

    def number_on_the_button_is_correct(self):
        checked_count = self.count_all_checked_checkbox()
        number_in_delete_button_text = self.text_delete_button()
        assert checked_count == number_in_delete_button_text, \
            f"Количество отмеченных чекбоксов ({checked_count}) не соответствует числу в тексте кнопки удаления ({number_in_delete_button_text})"

    def click_head_delete_button(self):
        self.page.locator(self.HEAD_DELETE_BUTTON).click()

    def click_head_not_availavle_delete_button(self):
        self.page.locator(self.NOT_AVAILABLE_HEAD_DELETE_BUTTON).click()

    def confirm_deletion(self):
        self.page.locator(self.CONFIRM_DELETE_BUTTON).click()

    def cancel_deletion(self):
        self.page.locator(self.CANCEL_DELETE_BUTTON).click()

    def product_removed_from_cart(self):
        self.all_checkbox_not_to_be_checked()

    def click_cross_button_delete(self):
        self.page.locator(self.CART_LIST_ROW_DELETE_BUTTON).nth(0).click()

    def click_cross_button_delete_in_changed_list(self):
        self.page.locator(self.CART_CHANGET_LIST_ROW_DELETE_BUTTON).nth(0).click()

    def click_cross_button_delete_in_not_availeble_list(self):
        self.page.locator(self.NOT_AVAILABLE_LIST_ROW_DELETE_BUTTON).nth(0).click()

    def save_name_product_in_change_info_list(self):
        element_cart = self.page.locator(".flexColumn.KitModal__Inner .ProductCartInfo__Title").nth(0)
        text_ct_cart = element_cart.inner_text()
        return text_ct_cart

    def save_name_product_in_cart_list(self):
        element_cart = self.page.locator(".ProductCartInfo__Title").nth(0)
        text_ct_cart = element_cart.inner_text()
        return text_ct_cart

    def save_name_product_in_not_availeble_list(self):
        element_cart = self.page.locator("div.CartUnavailableList .ProductCartInfo__Title").nth(0)
        text_ct_cart = element_cart.inner_text()
        return text_ct_cart

    def delete_product_by_cross(self):
        product_name = self.save_name_product_in_cart_list()
        self.click_cross_button_delete()
        expect(self.page.get_by_text(product_name)).not_to_be_visible()


    def calculate_total_price(self):
        # Находим все элементы .Price__Value внутри .AvailableList.CartPage__AvailableProductList
        prices = self.page.locator('.AvailableList.CartPage__AvailableProductList .Price__Value').all()

        # Суммируем значения цен
        total_price_listing = 0

        for price_element in prices:
            price_text = price_element.inner_text()

            # Преобразуем текст в число, убираем валютные символы и пробелы
            price_number = int(price_text.replace('\xa0', '').replace(' ', ''))

            # Проверяем, что цена больше 0
            while price_number <= 0:
                self.page.wait_for_selector('.AvailableList.CartPage__AvailableProductList .Price__Value')
                price_text = price_element.inner_text()
                price_number = int(price_text.replace('\xa0', '').replace(' ', ''))

            # Добавляем к общей сумме
            total_price_listing += price_number

        print(total_price_listing)
        return total_price_listing

    def get_cart_prices(self):
        prices = self.page.locator('.AvailableList.CartPage__AvailableProductList .Price__Value')
        prices_texts = prices.all_inner_texts()
        print(f"Found prices: {prices_texts}")  # Вывод всех найденных цен для проверки
        return [int(price.replace('\xa0', '').replace(' ', '')) for price in prices_texts]

    def compare_prices(self, total_price_listing):
        total_price_calculation_block_text = self.page.locator(self.ORDER_TOTAL_PRICE).inner_text()
        total_price_calculation_block = int(total_price_calculation_block_text.replace('\xa0', '').replace(' ', ''))
        print(total_price_calculation_block)
        print(type(total_price_calculation_block), type(total_price_listing))
        assert total_price_calculation_block == total_price_listing

    def order_price_is_zero(self):
        price = self.page.locator(self.ORDER_TOTAL_PRICE).inner_text()
        print(int(price))
        assert int(price) == 0

    def calculate_total_price_for_checked_products(self):
        try:
            # Находим все строки товаров
            product_rows = self.page.locator(
                '.AvailableList.CartPage__AvailableProductList .flexRow-JCSB-AIC.CartAvailableListRow').all()
            total_price_listing = 0

            # Проходим по всем строкам товаров
            for index, row in enumerate(product_rows):
                # Находим чекбокс и цену в строке товара
                checkbox = row.locator('.Checkbox__Input')
                price_element = row.locator('.Price__Value')

                # Проверяем, что чекбокс отмечен
                if checkbox.is_checked():
                    price_text = price_element.inner_text()

                    # Преобразуем текст в число, убираем валютные символы и пробелы
                    price_number = int(price_text.replace('\xa0', '').replace(' ', ''))

                    # Проверяем, что цена больше 0
                    while price_number <= 0:
                        self.page.wait_for_selector('.AvailableList.CartPage__AvailableProductList .Price__Value')
                        price_text = price_element.inner_text()
                        price_number = int(price_text.replace('\xa0', '').replace(' ', ''))

                    # Добавляем к общей сумме
                    total_price_listing += price_number

            print(total_price_listing)
            return total_price_listing

        except TimeoutError as e:
            print(f"Timeout error occurred: {e}")
            return 0

        except Exception as e:
            print(f"An error occurred: {e}")
            return 0

    def click_details_button(self):
        self.page.locator(self.DETALES_BUTTON).click()

    def click_ok_button(self):
        self.page.locator(self.OK_BUTTON).click()

    def click_print_button(self):
        self.page.locator(self.PRINT_BUTTON).click()

    def get_quantity_of_product(self):
        quantity = self.page.locator(".PrintProduct__Quantity")
        quantity_texts = quantity.all_inner_texts()
        print(f"Quantity found: {quantity_texts}")
        return [int(quantity.replace(' шт.', '')) for quantity in quantity_texts]

    def order_total_price(self):
        price_text = self.page.locator(self.ORDER_TOTAL_PRICE).inner_text()
        price = float(price_text.replace('\xa0', '').replace(' ', '').replace(',', '.'))
        return price

    def deletion_modal_not_visible(self):
        expect(self.page.locator(self.DETALES_BUTTON)).not_to_be_visible()

    def cart_is_empty(self):
        expect(self.page.locator(self.CART_IS_EMPTY)).to_be_visible()

    def click_home_button(self):
        self.page.locator(self.HOME_BUTTON).click()

    def click_autorization_button(self):
        self.page.locator(self.AUTORIZATION_BUTTON).click()

    def order_button_is_disabled(self):
        expect(self.page.locator(self.ORDER_BUTTON)).to_be_disabled()

    def promo_code_field_info(self):
        return self.page.locator(self.PROMO_CODE_FIELD_INFO)

    def cancel_promo_code(self):
        self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).click()

    def clear_promo_code_field_by_cross(self):
        self.page.locator(self.CLEAR_PROMO_CODE_FIELD_BUTTON).click()

    def promo_code_field(self):
        return self.page.locator(self.PROMO_CODE_FIELD)

    def hover_to_promo_code_hint(self):
        self.page.locator(self.PROMO_CODE_HINT_ICON).hover()

    def promo_code_hint_popup(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP)

    def promo_code_hint_popup_text(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP).inner_text()

    def info_change_block_activation(self, page, base_url):
        cart_page = CartPage(page)
        cart_page.add_to_cart_multiple_products(base_url)
        cart_page.open(base_url)
        cart_page.activate_valid_promo_code()
        cart_page.click_details_button()

    def not_available_for_order_block_activation(self, page, base_url):
        cart_page = CartPage(page)
        header = HeaderElement(page)
        cart_page.add_to_cart_multiple_stop_order_products(base_url)
        cart_page.open(base_url)
        header.change_location("Вахрушево")

    def click_back_to_cart_button(self):
        self.page.locator(self.BACK_TO_CART_BUTTON).click()



    # def select_random_checkbox(self):
    #     # Находим все чекбоксы на странице
    #     checkbox_locator = self.page.locator(self.CHECKBOX_PRODUCT)
    #     checkbox_count = checkbox_locator.count()
    #
    #     if checkbox_count == 0:
    #         raise ValueError("No checkboxes found on the page")
    #
    #     # Выбираем случайный индекс
    #     random_index = random.randint(0, checkbox_count - 1)
    #
    #     # Запоминаем локатор и индекс случайного чекбокса
    #     random_checkbox = checkbox_locator.nth(random_index)
    #
    #     return random_checkbox, random_index


    #TODO Cделать локаторы CHECKBOX_HEAD и CHECKBOX_PRODUCT уникальными, потому что они находят абсолютно одини и те же чекбоксы, после этого переназначить детей в первом и втором чек-боксе


    # def fill_promo_code
