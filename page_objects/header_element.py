import random
import playwright
import allure
from bs4 import BeautifulSoup
from playwright.sync_api import Error
from playwright.sync_api import TimeoutError

import pytest
from playwright.sync_api import expect


class HeaderElement:

    LOCATION_BUTTON = ".flexRow-AIC.LocationSelector"
    LOCATION_FIELD = ".flexColumn.KitModal__Inner .kit-input.Field__Input"
    SELECT_LOCATION = ".flexRow-AIC.LocatorCity"

    def __init__(self, page):
        self.page = page

    def open(self, url):
        with allure.step(f"Открываю {url}"):
            self.page.goto(url)

    @allure.step("Нажимаю на кнопку выбора локации")
    def click_location_button(self):
        self.page.locator(self.LOCATION_BUTTON).click()

    @allure.step("Меняю населенный пункт")
    def change_location(self, location):
        self.click_location_button()
        self.page.locator(self.LOCATION_FIELD).type(location)
        self.page.locator(self.SELECT_LOCATION).get_by_text(location).click()
