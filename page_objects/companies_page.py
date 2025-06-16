import allure
import re
from playwright.sync_api import expect, Page


class CompaniesPage:

    PATH = "/cabinet/companies/"

    COMPANY_CARD = ".CompanyCard.CompaniesPage__List__Item"
    COMPANY_CARD_BUTTON = ".CompanyCard__Button"
    INACTIVE_COMPANY_CARD_BUTTON = ".CompanyCard__Button span:has-text('Переключиться')"
    COMPANY_CARD_BUTTON_TEXT = ".CompanyCard__Button .Button__Text"
    RETAIL_COMPANY_CARD = ".CompanyCard.CompaniesPage__List__Item .CompanyCard__Block__Info span:has-text('Розничный')"
    BY_CONTRACT_COMPANY_CARD = ".CompanyCard.CompaniesPage__List__Item .CompanyCard__Block__Info span:has-text('По договору')"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открываю страницу Мои компании")
    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    @allure.step("Выбираю контрагента с не розничным типом цен")
    def select_company_with_not_retail_price(self, base_url):
        self.open(base_url)
        with allure.step("Нахожу компанию с не розничным типом цен"):
            by_contract_company_card = self.page.locator(self.BY_CONTRACT_COMPANY_CARD).nth(0)
            assert by_contract_company_card.is_visible(), "Блок не найден."

        with allure.step("Проверяю состояние кнопки и выбираю компанию, если она не выбрана"):
            company_card = by_contract_company_card.locator("xpath=ancestor::div[contains(@class, 'CompanyCard')]")
            button = company_card.locator(self.COMPANY_CARD_BUTTON)
            button_text = company_card.locator(self.COMPANY_CARD_BUTTON_TEXT)

            expect(button_text).to_be_visible()
            button_text_value = button_text.inner_text()

            if "Переключиться" in button_text_value:
                button.click()
                allure.attach("Компания успешно выбрана.", name="Состояние кнопки")
            else:
                allure.attach("Компания уже выбрана.", name="Состояние кнопки")

    @allure.step("Выбираю контрагента с розничным типом цен")
    def select_company_with_retail_price(self, base_url):
        self.open(base_url)
        with allure.step("Нахожу компанию с не розничным типом цен"):
            retail_company_card = self.page.locator(self.RETAIL_COMPANY_CARD).nth(0)
            assert retail_company_card.is_visible(), "Блок не найден."

        with allure.step("Проверяю состояние кнопки и выбираю компанию, если она не выбрана"):
            company_card = retail_company_card.locator("xpath=ancestor::div[contains(@class, 'CompanyCard')]")
            button = company_card.locator(self.COMPANY_CARD_BUTTON)
            button_text = company_card.locator(self.COMPANY_CARD_BUTTON_TEXT)

            expect(button_text).to_be_visible()
            button_text_value = button_text.inner_text()

            if "Переключиться" in button_text_value:
                button.click()
                allure.attach("Компания успешно выбрана.", name="Состояние кнопки")
            else:
                allure.attach("Компания уже выбрана.", name="Состояние кнопки")

    @allure.step("Переключаюсь на компанию с иным типом цен")
    def select_a_company_with_a_different_type_of_pricing(self, base_url):
        self.open(base_url)
        with allure.step("Нахожу компанию с не розничным типом цен"):
            by_contract_company_card = self.page.locator(self.BY_CONTRACT_COMPANY_CARD).nth(0)
            assert by_contract_company_card.is_visible(), "Блок не найден."

        with allure.step("Проверяю состояние кнопки и выбираю компанию, если она не выбрана"):
            company_card = by_contract_company_card.locator("xpath=ancestor::div[contains(@class, 'CompanyCard')]")
            button = company_card.locator(self.COMPANY_CARD_BUTTON)
            button_text = company_card.locator(self.COMPANY_CARD_BUTTON_TEXT)

            expect(button_text).to_be_visible()
            button_text_value = button_text.inner_text()

            if "Переключиться" in button_text_value:
                button.click()
                allure.attach("Компания успешно выбрана.", name="Состояние кнопки")
            else:
                self.select_company_with_retail_price(base_url)

    @allure.step("Переключаюсь на первую невыбранную коммпанию")
    def select_other_company(self, base_url):
        self.open(base_url)
        self.page.locator(self.INACTIVE_COMPANY_CARD_BUTTON).first().click()
                # cards = self.page.locator()
                # for card in cards:
                # #первая компания с кнопкой переключится
                # button.click()

        # with allure.step("Выбираю компанию, если она не выбрана"):
        #     selection_state = parent_block.locator(self.COMPANY_CARD_BUTTON_TEXT).inner_text()
        #     if selection_state == "Выбрана":
        #         pass
        #     else:
        #         parent_block.locator(self.COMPANY_CARD_BUTTON).click()
        #     actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()
        #     actual_info_listing = f"{actual_title}, {actual_description}"
        #
        # with allure.step("Нажимаю кнопку Выбрать"):
        #     self.page.locator(self.ADRESS_SELECTION_BUTTON).click()