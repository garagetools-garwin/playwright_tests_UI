import random
import testit
import playwright
from bs4 import BeautifulSoup
from playwright.sync_api import Error, Page
from playwright.sync_api import TimeoutError

import pytest
import allure
from playwright.sync_api import expect

from page_objects.header_element import HeaderElement


class ProductCartElement:

    PATH = "/tovar/razem-papa-naruzhnaya-rezba-1-2-latun"

    """Промокод"""
    ADD_TO_CART_BUTTON = ".ProductDetailControls__AddToCartButton.Button.flexRow.size--normal.color--primary"


    def __init__(self, page: Page):
        self.page = page

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    @allure.step("Добавляю товар в корзину")
    def add_to_cart(self):
        self.page.locator(self.ADD_TO_CART_BUTTON).click()

