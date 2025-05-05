import allure


class HeaderElement:

    LOCATION_BUTTON = ".flexRow-AIC.LocationSelector"
    LOCATION_FIELD = ".flexColumn.KitModal__Inner .kit-input.Field__Input"
    SELECT_LOCATION = ".flexRow-AIC.LocatorCity"
    #autorized
    ACCOUNT_BUTTON = ".NavigationButton.Header__Navigation__Button.Header__LoginButton.Header__UserButton"
    ACCOUNT_MENU = "div.Header__AuthMenu"
    CUSTOMER_SWITCH_BUTTON = "button.AuthMenuHeader__SwitcherButton"
    CUSTOMER_IN_LIST = "button.AuthMenuCustomersButton"
    INACTIVE_CUSTOMER_IN_LIST = "button.AuthMenuCustomersButton:not([class*='--is-selected'])"
    SELECTED_COMPANY_NAME = ".Header__UserButton .NavigationButton__Text"
    ACCOUNT_BUTTONS = "button.AuthMenuAccounts__Button"
    MY_ACCOUNT = 'div.AuthMenuAccounts button:has(span.AuthMenuAccounts__Subtitle)'
    OTHER_ACCOUNT = 'div.AuthMenuAccounts button:not(:has(span.AuthMenuAccounts__Subtitle))'


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

    @allure.step("Активирую меню аккаунта")
    def account_header_menu_activation(self):
        self.page.locator(self.ACCOUNT_BUTTON).hover()
        # expect(self.page.locator(self.ACCOUNT_MENU)).to_be_visible()

    @allure.step("Открываю список контрагентов")
    def get_customers_list(self):
        self.page.locator(self.CUSTOMER_SWITCH_BUTTON).click()

    @allure.step("Выбираю контрагента")
    def select_customer(self):
        self.page.locator(self.INACTIVE_CUSTOMER_IN_LIST).nth(0).click()

    @allure.step("Переключаю контрагента")
    def switch_customer(self):
        self.account_header_menu_activation()
        # self.get_customers_list()
        self.select_customer()

    # Локатор для названия выбранной компании
    def company_name_text(self):
        return self.page.locator(self.SELECTED_COMPANY_NAME).inner_text()

    @allure.step("Переключаюсь на аккаунт пользователя")
    def switching_to_user_account(self):
        self.account_header_menu_activation()
        self.page.locator(self.MY_ACCOUNT).click()

    @allure.step("Переключаюсь на приглашенный аккаунт")
    def switching_to_other_account(self):
        self.account_header_menu_activation()
        self.page.locator(self.OTHER_ACCOUNT).click()

