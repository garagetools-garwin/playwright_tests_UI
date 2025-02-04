import time

import allure
import os

import requests


class AutorizationModalElement:

    PATH = "/cart"
    AUTORIZATION_MODAL = ".flexColumn.KitModal__Inner"
    GET_CODE_BUTTON = ".Button.size--big.color--primary"


    def __init__(self, page):
        self.page = page
        self.autorization_modal = page.locator(self.AUTORIZATION_MODAL)


    #TODO Переделать open. Должен окрыватся при нажатии на иконку "Войти"
    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    @allure.step("Авторизуюсь через mail.ru")
    def get_autorization_code_mail_ru(self):
        # Открываем новую вкладку
        context = self.page.context
        new_page = context.new_page()
        user_pass = os.getenv('USER_PASS')
        # Переходим на страницу авторизации в новой вкладке
        new_page.goto("https://account.mail.ru")
        new_page.locator('[name="username"]').fill("testgarwin_yur@mail.ru")
        new_page.locator('[data-test-id="next-button"]').click()
        new_page.locator('[type="password"]').fill(f"{user_pass}")
        new_page.locator('[data-test-id="submit-button"]').click()
        new_page.get_by_text("Авторизация на сайте Гарвин").nth(0).click()
        code_auth = new_page.locator('span[style="font-weight:bold;"]').nth(0).inner_text()

        new_page.close()

        return code_auth

    @allure.step("Отправляю код авторизации")
    def cart_autorization_send_code_mail_ru(self):
        self.page.locator(".kit-input.Field__Input").nth(1).fill("testgarwin_yur@mail.ru")
        self.page.locator(".Button.size--big.color--primary").click()

    @allure.step("Отправляю код авторизации")
    def cart_autorization_send_code_testmail_app(self):
        testmail_adress = os.getenv("TESTMAIL_ADRESS")
        self.page.locator(".kit-input.Field__Input").nth(1).fill(f"{testmail_adress}")
        self.page.locator(".Button.size--big.color--primary").click()

    @allure.step("Отправляю код авторизации")
    def cart_autorization_send_code_testmail_app_empty(self):
        testmail_adress = os.getenv("TESTMAIL_ADRESS_EMPTY")
        self.page.locator(".kit-input.Field__Input").nth(1).fill(f"{testmail_adress}")
        self.page.locator(".Button.size--big.color--primary").click()

    @allure.step("Завершаю авторизацию")
    def complete_autorization(self, code):
        self.page.locator(".kit-input.Field__Input").nth(1).fill(code)
        self.page.locator(".AuthConfirm__Form__ConfirmButton.Button.size--big.color--primary").click()

    @allure.step("Авторизуюсь через testmail.app")
    def get_autorization_code_testmail_app(self):
        time.sleep(15)
        testmail_json = os.getenv("TESTMAIL_JSON")
        response = requests.get(url=f"{testmail_json}")
        response_json = response.json()
        email_text = response_json["emails"][0]["text"]
        code = email_text.split(" ")[1]
        print(code)
        return code

    @allure.step("Авторизуюсь через testmail.app")
    def get_autorization_code_testmail_app_empty(self):
        time.sleep(15)
        testmail_json = os.getenv("TESTMAIL_JSON_EMPTY")
        response = requests.get(url=f"{testmail_json}")
        response_json = response.json()
        email_text = response_json["emails"][0]["text"]
        code = email_text.split(" ")[1]
        print(code)
        return code

    def autorization_testmail_app(self):
        self.cart_autorization_send_code_testmail_app()
        code = self.get_autorization_code_testmail_app()
        self.complete_autorization(code)

    def autorization_testmail_app_empty(self):
        self.cart_autorization_send_code_testmail_app_empty()
        code = self.get_autorization_code_testmail_app_empty()
        self.complete_autorization(code)


    # def autorization_modal_is_visible(self):
    #     self.page.locator(self.AUTORIZATION_MODAL).is_visible()


