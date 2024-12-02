import random
import testit
import playwright
from bs4 import BeautifulSoup
from playwright.sync_api import Error
from playwright.sync_api import TimeoutError

import pytest
import allure
from playwright.sync_api import expect

from page_objects.header_element import HeaderElement


class CheckoutPage:

    PATH = "/checkout"

    """Промокод"""
    PROMO_CODE_FIELD_INFO = ".Field__Info .Field__Text"
    CLEAR_PROMO_CODE_FIELD_BUTTON = ".flexRow-C.FieldControls__Button.active"
    PROMO_CODE_FIELD = ".kit-input.Field__Input.disable-label"
    PROMO_CODE_FIELD_CHECK = ".Field.PromoWidget__Field.is-small.has-controls"
    PROMO_CODE_HINT_ICON = "div.Tooltip__Icon"
    PROMO_CODE_HINT_POPUP = ".Tooltip__Inner.v-enter-to .Tooltip__Content"
    CANCEL_PROMO_CODE_BUTTON = ".flexRow-AIC.PromoWidget__CancelButton"
    PROMO_CODE_TOGGLE_BUTTON = ".PromoWidget__ToggleButton"
    PROMO_CODE_APPLY_BUTTON = ".PromoWidget__SubmitButton.Button.size--normal.color--secondary"
    PRODUCT_PRICE = "p.CheckoutDeliveryProduct__Price"

    """Чек-аут"""
    ORDER_BUTTON = ".OrderTotal__Button.Button.size--medium.color--primary"

    def __init__(self, page):
        self.page = page

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    """ Блок 'Промокод' """

    @allure.step("Активирую валидный промокод")
    def price_changes_with_a_promo_code(self):
        self.open_promo_code_bar()
        self.check_promo_code()


    @allure.step("Отменяю промокод если он был установлен")
    def check_promo_code(self):
        self.open_promo_code_bar()
        if self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).is_visible():
            self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).click()
        else:
            return
            # self.fill_valid_promo_code()
            # self.click_apply_button()

    @allure.step("Открываю блок 'Промокод'")
    def open_promo_code_bar(self):
        self.page.locator(self.PROMO_CODE_TOGGLE_BUTTON).click()

    @allure.step("Закрываю блок 'Промокод'")
    def close_promo_code_bar(self):
        self.open_promo_code_bar()

    def promo_code_bar(self):
        return self.page.locator(self.PROMO_CODE_TOGGLE_BUTTON)

    @allure.step("Ввожу валидный промокод")
    def fill_valid_promo_code(self):
        self.page.locator(self.PROMO_CODE_FIELD).fill("НАЧАЛО")

    @allure.step("Ввожу невалидный промокод")
    def fill_invalid_promo_code(self):
        self.page.locator(self.PROMO_CODE_FIELD).fill("12345DF")

    @allure.step("Нажимаю 'Применить'")
    def click_apply_button(self):
        self.page.locator(self.PROMO_CODE_APPLY_BUTTON).click()

    # Версия активации когда не нужно запоминать цену
    # @allure.step("Активирую валидный промокод")
    # def activate_valid_promo_code(self):
    #     self.open_promo_code_bar()
    #     self.check_promo_code()
    #     self.fill_valid_promo_code()
    #     self.click_apply_button()


    @allure.step("Активирую валидный промокод")
    def activate_valid_promo_code(self):
        self.fill_valid_promo_code()
        self.click_apply_button()

    @allure.step("Активирую невалидный промокод")
    def activate_invalid_promo_code(self):
        # self.open_promo_code_bar()
        self.fill_invalid_promo_code()
        self.click_apply_button()

    # Подсказка поля промокод
    def promo_code_field_info(self):
        return self.page.locator(self.PROMO_CODE_FIELD_INFO)

    @allure.step("Отменяю примененный промокод")
    def cancel_promo_code(self):
        self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).click()

    @allure.step("Очищаю проле Промокод нажатием на крестик")
    def clear_promo_code_field_by_cross(self):
        self.page.locator(self.CLEAR_PROMO_CODE_FIELD_BUTTON).click()

    # Поле промокод
    def promo_code_field(self):
        return self.page.locator(self.PROMO_CODE_FIELD_CHECK)

    @allure.step("Навожу курсор на подсказку")
    def hover_to_promo_code_hint(self):
        self.page.locator(self.PROMO_CODE_HINT_ICON).hover()

    # Подсказка
    def promo_code_hint_popup(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP)

    # Текст подсказки
    def promo_code_hint_popup_text(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP).inner_text()


    """Блок Калькуляции"""


    # @allure.step("Запоминаю стоимость скидки")
    # def discounted_price(self):
    #     text_discounted_price = self.page.locator(self.PRODUCT_PRICE_DISCOUNTED).inner_text()
    #     discounted_price_number = float(text_discounted_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.'))
    #     return discounted_price_number


    @allure.step("Запоминаю первоначальную стоимость товара")
    def base_price(self):
        text_base_price = self.page.locator(self.PRODUCT_PRICE).inner_text()
        base_price_number = float(text_base_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽/шт.', ''))
        return base_price_number
