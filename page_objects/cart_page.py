import random
import playwright
from bs4 import BeautifulSoup
from playwright.sync_api import Error
from playwright.sync_api import TimeoutError

import pytest
from playwright.sync_api import expect


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
    LIST_ROW_DELETE_BUTTON = ".CartAvailableListRow__RemoveBtn"
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


    def __init__(self, page):
        self.page = page
        self.change_info_block = page.locator(self.CHANGE_INFO_BLOCK)
        self.change_info_modal = page.locator(self.CHANGE_INF0_MODAL)
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

    def open_promocode_bar(self):
        self.page.locator(".CartPromo__ToggleButton").click()

    def fill_promocode(self):
        self.page.locator(".kit-input.Field__Input.disable-label").nth(1).fill("НАЧАЛО")

    def click_apply_button(self):
        self.page.locator("//*[text()='Применить']").click()

    def activate_promocode(self):
        self.open_promocode_bar()
        self.fill_promocode()
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

    def confirm_deletion(self):
        self.page.locator(self.CONFIRM_DELETE_BUTTON).click()

    def cancel_deletion(self):
        self.page.locator(self.CANCEL_DELETE_BUTTON).click()

    def product_removed_from_cart(self):
        self.all_checkbox_not_to_be_checked()

    def click_cross_button_delete(self):
        self.page.locator(self.LIST_ROW_DELETE_BUTTON).nth(0).click()

    def save_name_product(self):
        element_cart = self.page.locator(".ProductCartInfo__Title").nth(0)
        text_ct_cart = element_cart.inner_text()
        return text_ct_cart

    def delete_product_by_cross(self):
        product_name = self.save_name_product()
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
        price = int(price_text.replace('\xa0', '').replace(' ', ''))
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


    # def fill_promocode
