import pytest


class AutorizationModalElement:

    PATH = "/cart"
    AUTORIZATION_MODAL = ".flexColumn.KitModal__Inner"
    GET_CODE_BUTTON = ".Button.size--big.color--primary"


    def __init__(self, page):
        self.page = page
        self.autorization_modal = page.locator(self.AUTORIZATION_MODAL)


    #TODO Переделать open. Должен окрыватся при нажатии на иконку "Войти"
    def open(self, url):
        self.page.goto(url + self.PATH)

    def get_autorization_code_mail_ru(self):
        # Открываем новую вкладку
        context = self.page.context
        new_page = context.new_page()

        # Переходим на страницу авторизации в новой вкладке
        new_page.goto("https://account.mail.ru")
        new_page.locator('[name="username"]').fill("testgarwin_yur@mail.ru")
        new_page.locator('[data-test-id="next-button"]').click()
        new_page.locator('[type="password"]').fill("MuIPU&iasb21")
        new_page.locator('[data-test-id="submit-button"]').click()
        new_page.get_by_text("Авторизация на сайте Гарвин").nth(0).click()
        code = new_page.locator('span[style="font-weight:bold;"]').nth(0).inner_text()

        new_page.close()

        return code

    def cart_autorization_send_code(self):
        self.page.locator(".kit-input.Field__Input").nth(1).fill("testgarwin_yur@mail.ru")
        self.page.locator(".Button.size--big.color--primary").click()

    def complete_autorization(self, code):
        self.page.locator(".kit-input.Field__Input").nth(1).fill(code)
        self.page.locator(".AuthConfirm__Form__ConfirmButton.Button.size--big.color--primary").click()




    # def autorization_modal_is_visible(self):
    #     self.page.locator(self.AUTORIZATION_MODAL).is_visible()


