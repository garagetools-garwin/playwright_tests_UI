import random
import allure
import re
from faker import Faker
from playwright.sync_api import expect

fake = Faker('ru_RU')


class PurchasePage:

    PATH = "/cabinet/purchase/"

    ORDER_BUTTON = ".OrderTotal__Button.Button.size--medium.color--primary"

    def __init__(self, page):
        self.page = page

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    @allure.step("Извлекаю номер заказа")
    def memorize_the_order_number(self):
        return self.page.locator("p.OrderSummary__Number").inner_text().split("Номер заказа: ")[1]



