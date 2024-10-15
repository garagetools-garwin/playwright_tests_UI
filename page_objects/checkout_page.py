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
    PROMO_CODE_FIELD_INFO = ".Field.CartPromo__Field .Field__Info .Field__Text"
    CLEAR_PROMO_CODE_FIELD_BUTTON = ".flexRow-C.FieldControls__Button.active"
    PROMO_CODE_FIELD = ".kit-input.Field__Input.disable-label"
    PROMO_CODE_HINT_ICON = ".flexRow-AIC.Tooltip.CartPromo__Tooltip"
    PROMO_CODE_HINT_POPUP = ".Tooltip__Inner.v-enter-to .Tooltip__Content"
    CANCEL_PROMO_CODE_BUTTON = ".flexRow-AIC.PromoWidget__CancelButton"
    PROMO_CODE_TOGGLE_BUTTON = ".PromoWidget__ToggleButton"
    PROMO_CODE_APPLY_BUTTON = ".PromoWidget__SubmitButton.Button.size--normal.color--secondary"

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
        if self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).is_visible():
            self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).click()
        else:
            self.fill_valid_promo_code()
            self.click_apply_button()

    @allure.step("Открываю блок 'Промокод'")
    def open_promo_code_bar(self):
        self.page.locator(self.PROMO_CODE_TOGGLE_BUTTON).click()

    @allure.step("Закрываю блок 'Промокод'")
    def close_promo_code_bar(self):
        self.open_promo_code_bar()

    def promo_code_bar(self):
        return self.page.locator(".CartPromo__ToggleButton")

    @allure.step("Ввожу валидный промокод")
    def fill_valid_promo_code(self):
        self.page.locator(self.PROMO_CODE_FIELD).fill("НАЧАЛО")

    @allure.step("Ввожу невалидный промокод")
    def fill_invalid_promo_code(self):
        self.page.locator(self.PROMO_CODE_FIELD).fill("12345DF")

    @allure.step("Нажимаю 'Применить'")
    def click_apply_button(self):
        self.page.locator(self.PROMO_CODE_APPLY_BUTTON).click()

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
        return self.page.locator(self.PROMO_CODE_FIELD)

    @allure.step("Навожу курсор на подсказку")
    def hover_to_promo_code_hint(self):
        self.page.locator(self.PROMO_CODE_HINT_ICON).hover()

    # Подсказка
    def promo_code_hint_popup(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP)

    # Текст подсказки
    def promo_code_hint_popup_text(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP).inner_text()

