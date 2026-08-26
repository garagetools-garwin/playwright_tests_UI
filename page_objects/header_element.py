import allure
from playwright.sync_api import Page, expect


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
    # Кнопка аккаунта, на который сейчас МОЖНО переключиться: у текущего аккаунта
    # кнопка отключена (disabled), поэтому доступная всегда ровно одна
    AVAILABLE_ACCOUNT = 'div.AuthMenuAccounts button:not([disabled])'
    # Кнопка текущего аккаунта — она отключена; по ней узнаём, где мы сейчас
    CURRENT_ACCOUNT = 'div.AuthMenuAccounts button[disabled] span.AuthMenuAccounts__Title'


    def __init__(self, page: Page):
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
        # Меню раскрывается по наведению: контейнер имеет нулевую высоту и
        # "проявляется" через opacity, поэтому проверка to_be_visible тут не работает
        # (Playwright считает такой контейнер скрытым). Ждём именно раскрытия — opacity=1,
        # иначе клик уходит в ещё прозрачное меню и висит до таймаута (падало в CI).
        self.page.locator(self.ACCOUNT_BUTTON).hover()
        expect(self.page.locator(self.ACCOUNT_MENU)).to_have_css("opacity", "1")

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
        my_account = self.page.locator(self.MY_ACCOUNT)
        # наводимся на сам пункт: мышь остаётся внутри меню, и оно не схлопывается
        my_account.hover()
        my_account.click()

    @allure.step("Переключаюсь на доступный аккаунт")
    def switching_to_available_account(self):
        """Переключается на тот аккаунт, который сейчас не выбран.

        Не зависит от того, на каком аккаунте застали сессию: кнопка текущего
        аккаунта отключена, поэтому жмём единственную доступную. Два вызова
        подряд возвращают сессию в исходное состояние.
        Возвращает название аккаунта, на который переключились.
        """
        self.account_header_menu_activation()
        account = self.page.locator(self.AVAILABLE_ACCOUNT)
        expect(account).to_be_enabled()
        name = account.locator("span.AuthMenuAccounts__Title").inner_text().strip()
        # наводимся на сам пункт: мышь остаётся внутри меню, и оно не схлопывается
        account.hover()
        account.click()
        # Подтверждаем переключение по активному аккаунту в меню, а не по шапке:
        # в шапке название контрагента, а один и тот же контрагент может быть
        # выбран в обоих аккаунтах — тогда текст шапки не меняется
        self.account_header_menu_activation()
        expect(self.page.locator(self.CURRENT_ACCOUNT)).to_have_text(name)
        return name

    @allure.step("Узнаю текущий аккаунт")
    def current_account_name(self):
        """Название аккаунта, в котором сейчас сессия.

        Определяем по отключённой кнопке в меню, а не по шапке: в шапке выводится
        название выбранного контрагента, а оно меняется и внутри одного аккаунта.
        """
        self.account_header_menu_activation()
        return self.page.locator(self.CURRENT_ACCOUNT).inner_text().strip()

    @allure.step("Возвращаю исходный аккаунт")
    def restore_account(self, account_name):
        """Возвращает сессию на аккаунт account_name, если она не на нём.

        Зовётся из finally: тест не должен оставлять сессию на чужом аккаунте
        даже при падении, иначе следующий прогон стартует не с того состояния.
        """
        if self.current_account_name() == account_name:
            return False
        self.switching_to_available_account()
        return True

    @allure.step("Переключаюсь на приглашенный аккаунт")
    def switching_to_other_account(self):
        self.account_header_menu_activation()
        other_account = self.page.locator(self.OTHER_ACCOUNT)
        # наводимся на сам пункт: мышь остаётся внутри меню, и оно не схлопывается
        other_account.hover()
        other_account.click()

