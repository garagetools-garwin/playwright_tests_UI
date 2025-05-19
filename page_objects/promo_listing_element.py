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


class PromoListingElement:

    PATH = "/promos"

    PROMO_CARD = "a.PromoCard__Link"

    def __init__(self, page):
        self.page = page

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    @allure.step("Перехожу в первую акцию в листинге")
    def click_first_promo(self):
        self.page.locator(self.PROMO_CARD).nth(0).click()

