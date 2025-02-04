import random
import allure
import re
from faker import Faker
from playwright.sync_api import expect

fake = Faker('ru_RU')


class CheckoutPage:

    PATH = "/checkout"

    ORDER_BUTTON = ".OrderTotal__Button.Button.size--medium.color--primary"

    def __init__(self, page):
        self.page = page

        self.buyer_and_recipient_block = BuyerAndRecipientBlock(page)
        self.recipient_listing = RecipientListing(page)
        self.add_recipient_modal = AddRecipientModal(page)
        self.edit_recipient_modal = EditRecipientModal(page)
        self.delete_conformation_modal = DeleteConformationModal(page)

        self.obtaining_block = ObtainingBlock(page)
        self.adress_listing = AdressListing(page)
        self.map = Map(page)

        self.delivery_block = DeliveryBlock(page)

        self.calculation_block = CalculationBlock(page)
        self.promo_code = PromoCode(page)

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)


"""Блок Покупатель и получатель"""


class BuyerAndRecipientBlock:

    ADD_FIRST_RECIPIENT_BUTTON = "#contacts .SectionInfo__ButtonAdd"
    RECIPIENT_CHANGE_BUTTON = "#contacts .SectionInfo__Button"
    CUSTOMER_NAME = "#contacts .CheckoutSection__Custom span.SectionInfo__Title"
    RECIPIENT_INFO = "#contacts .CheckoutSection__Body span.SectionInfo__Title"

    def __init__(self, page):
        self.page = page

    @allure.step("Открываю окно Нового получателя")
    def click_add_first_recipient_button(self):
        self.page.locator(self.ADD_FIRST_RECIPIENT_BUTTON).click()



"""Листинг получателей"""


class RecipientListing:

    RECIPIENT_LISTING_MODAL = ".RecipientSelection .flexColumn.KitModal__Inner"
    ADD_RECIPIENT_BUTTON = "button.RecipientSelection__ButtonAdd"
    SELECTED_RADIO_BUTTON = "input[type='radio']:checked"
    UNSELECTED_RADIO_BUTTON = ".Radio__Inner >> input[type='radio']:not(:checked)"
    RECIPIENT_BLOCK = "#delivery-point"
    INFO_TITLE = ".RecipientSelection__InfoTitle"
    INFO_DESCRIPTION = ".RecipientSelection__InfoDescription"
    CHECKED_RECIPIENT_BLOCK = "li#delivery-point:has(input[type='radio']:checked)"
    RECIPIENT_SELECTION_BUTTON = "button.RecipientSelection__ButtonChange"
    ACTION_MENU = ".RecipientSelection__ButtonEdit"
    ACTION_MENU_MODAL = ".RecipientSelection__Item__Tooltip.--open-tooltip"
    EDIT_BUTTON = ".RecipientSelection__Item__Tooltip.--open-tooltip span:has-text('Редактировать')"
    DELETE_BUTTON = ".RecipientSelection__Item__Tooltip.--open-tooltip span:has-text('Удалить')"
    CHANGE_RECIPIENT_MODAL = "p:has-text('Изменить получателя')"
    DELETE_CONFIRMATION_MODAL = "p:has-text('Вы уверены, что хотите удалить получателя?')"

    def __init__(self, page):
        self.page = page
        self.buyer_and_recipient_block = BuyerAndRecipientBlock

    @allure.step("Открываю листинг получателей")
    def open_recipient_listing(self):
        self.page.locator(self.buyer_and_recipient_block.RECIPIENT_CHANGE_BUTTON).click()
        with allure.step("Проверяю, что листинг пользователей открыт"):
            expect(self.page.locator(self.RECIPIENT_LISTING_MODAL)).to_be_visible()

    @allure.step("Выбираю неактивного пользователя")
    def switch_on_inactive_recipient(self):
        # Локатор для первого невыбранного радио-баттона
        radio_locator = self.page.locator(self.UNSELECTED_RADIO_BUTTON).nth(0)

        # Клик по соседнему span.Radio__Button
        radio_locator.locator("xpath=..").locator("span.Radio__Button").click()

    @allure.step("Выбираю неактичного пользователя")
    def select_inactive_recipient(self):
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()
            actual_info_listing = f"{actual_title}, {actual_description}"

        with allure.step("Нажимаю кнопку Выбрать"):
            self.page.locator(self.RECIPIENT_SELECTION_BUTTON).click()

        with allure.step("Извлекаю текст из блока Получать"):
            actual_info_check_out = self.page.locator(self.buyer_and_recipient_block.RECIPIENT_INFO).inner_text()

        with allure.step("Сравниваю информацию в блоке Получатель с получателем выбранным в листинге "):
            assert actual_info_check_out.lower() == actual_info_listing.lower(), f"Expected '{actual_info_listing}', but got '{actual_info_check_out}'"

    @allure.step("Открываю экшн меню")
    def open_action_menu(self):
        self.page.locator(self.ACTION_MENU).nth(0).click()
        with allure.step("Проверяю, что экшн меню открыто"):
            expect(self.page.locator(self.ACTION_MENU_MODAL)).to_be_enabled()
        with allure.step("Проверяю, что в меню отображаются кнопки Редактировать и Удалить"):
            expect(self.page.locator(self.EDIT_BUTTON)).to_be_visible()
            expect(self.page.locator(self.DELETE_BUTTON)).to_be_visible()

    @allure.step("Нажимаю на Редактировать")
    def click_edit_button(self):
        self.page.locator(self.EDIT_BUTTON).click()
        with allure.step("Проверяю, что окно Изменить получателя отображается на странице"):
            expect(self.page.locator(self.CHANGE_RECIPIENT_MODAL)).to_be_visible()

    @allure.step("Нажимаю на Удалить")
    def click_delete_button(self):
        self.page.locator(self.DELETE_BUTTON).click()
        with allure.step("Проверяю, что окно подтверждения удаления отображается на странице"):
            expect(self.page.locator(self.DELETE_CONFIRMATION_MODAL)).to_be_visible()


"""Модалка Новый получатель"""


class AddRecipientModal:

    RECIPIENT_MODAL = ".RecipientSelectionAdd .flexColumn.KitModal__Inner"
    NAME_FIELD = "div.RecipientSelectionAdd__Input input[type='text']"
    TEL_FIELD = "div.RecipientSelectionAdd__Input input[type='tel']"
    EMAIL_FIELD = "div.RecipientSelectionAdd__Input input[type='email']"
    SAVE_RECIPIENT_BUTTON = "button.RecipientSelectionAdd__Button"
    CLOSE_BUTTON = ".RecipientSelectionAdd .KitModal__Closer"

    def __init__(self, page):
        self.page = page
        self.recipient_listing = RecipientListing
        self.add_recipient_modal = AddRecipientModal
        self.buyer_and_recipient_block = BuyerAndRecipientBlock

    @allure.step("Закрываю модальное окно нового получателя")
    def add_recipient_modal_(self):
        return self.page.locator(self.RECIPIENT_MODAL)

    @allure.step("Закрываю модальное окно нового получателя")
    def close_new_recipient_modal(self):
        self.page.locator(self.CLOSE_BUTTON).click()
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.RECIPIENT_MODAL)).not_to_be_visible()

    @allure.step("Закрываю модальное окно нового получателя")
    def close_new_recipient_modal2(self):
        self.page.mouse.click(0, 0)
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.RECIPIENT_MODAL)).not_to_be_visible()

    @allure.step("Заполняю поля сгенерированными данными")
    def fill_in_data(self):
        name_first = "вывЫвыв wdSdsdsdsd-вавава вававава'ывыывывывывывывывывывывывывывывыывывывывывыываывывывывв"
        # Генерация случайных первых трех букв кириллицы
        cyrillic_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        random_letters = ''.join(random.choices(cyrillic_letters, k=3))
        name = random_letters + name_first[3:]  # Замена первых трех символов
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        email = fake.email()

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)
        self.page.locator(self.EMAIL_FIELD).fill(email)

        return name, phone, email

    @allure.step("Заполняю поля сгенерированными данными")
    def fill_in_data_randomize(self):
        name = fake.name()
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        email = fake.email()

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)
        self.page.locator(self.EMAIL_FIELD).fill(email)

        return name, phone, email

    @allure.step("Заполняю поля сгенерированными данными")
    def fill_in_part_of_data_randomize(self):
        name = fake.name()
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)

        return name, phone

    @allure.step("Сохраняю нового получателя")
    def save_new_recipient(self):
        self.page.locator(self.SAVE_RECIPIENT_BUTTON).click()
        with allure.step("Проверяю, что модальное окно нового пользователя закрыто"):
            expect(self.page.locator(self.RECIPIENT_MODAL)).not_to_be_visible()
        with allure.step("Проверяю, что листинг пользователей закрыт"):
            expect(self.page.locator(self.recipient_listing.RECIPIENT_LISTING_MODAL)).not_to_be_visible()

    @allure.step("Добавляю получателя")
    def add_recipient(self):
        self.page.locator(self.recipient_listing.ADD_RECIPIENT_BUTTON).click()
        with allure.step("Проверяю, что модальное окно нового пользователя открыто"):
            expect(self.page.locator(self.add_recipient_modal.RECIPIENT_MODAL)).to_be_visible()

    @allure.step("Проверяю текст в блоке получателя")
    def verify_recipient_info(self, expected_info):
        actual_info = self.page.locator(self.buyer_and_recipient_block.RECIPIENT_INFO).inner_text()
        # expected_info = expected_info.replace(', ,', ',')
        print(actual_info.lower())
        print(expected_info.lower())
        assert actual_info.lower() == expected_info.lower(), f"Expected '{expected_info}', but got '{actual_info}'"

    @allure.step(
        "Проверяю, что новый получатель появился в листинге, его информация соответствует заданной, он активен")
    def verify_selected_recipient_info(self, expected_title, expected_description):
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.recipient_listing.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.recipient_listing.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.recipient_listing.INFO_DESCRIPTION).inner_text()

        with allure.step("Сравниваю с ожидаемыми значениями"):
            assert actual_title.lower() == expected_title.lower(), f"Ожидалось: {expected_title}, Получено: {actual_title}"
            assert actual_description == expected_description, f"Ожидалось: {expected_description}, Получено: {actual_description}"

    @allure.step("Создаю нового получателя")
    def create_recipient(self,base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        checkout_page.recipient_listing.open_recipient_listing()
        checkout_page.add_recipient_modal.add_recipient()
        with allure.step("Ввожу текст в котором включены все допустимые буквы и символы, их максимальное количество"):
            name, phone, email = checkout_page.add_recipient_modal.fill_in_data()
        checkout_page.add_recipient_modal.save_new_recipient()
        with allure.step("Формирую ожидаемый текст"):
            expected_info = f"{name}, {email}, {phone}"
        checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
        checkout_page.recipient_listing.open_recipient_listing()

        with allure.step("Формирую ожидаемый текст"):
            expected_info_title = name
            expected_info_description = f"{email}, {phone}"
        with allure.step("Проверяю информацию о выбранном получателе"):
            checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title,
                                                                             expected_info_description)

"""Модалка Изменить получателя"""


class EditRecipientModal:

    RECIPIENT_MODAL = ".RecipientSelectionEdit .flexColumn.KitModal__Inner"
    NAME_FIELD = "div.RecipientSelectionEdit__Input input[type='text']"
    TEL_FIELD = "div.RecipientSelectionEdit__Input input[type='tel']"
    EMAIL_FIELD = "div.RecipientSelectionEdit__Input input[type='email']"
    SAVE_RECIPIENT_BUTTON = "button.RecipientSelectionEdit__Button"
    CLOSE_BUTTON = ".RecipientSelectionEdit .KitModal__Closer"

    def __init__(self, page):
        self.page = page
        self.recipient_listing = RecipientListing

    @allure.step("Закрываю модальное окно изменения получателя")
    def close_edit_recipient_modal(self):
        self.page.locator(self.CLOSE_BUTTON).click()
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.RECIPIENT_MODAL)).not_to_be_visible()

    @allure.step("Закрываю модальное окно изменения получателя")
    def close_edit_recipient_modal2(self):
        self.page.mouse.click(0, 0)
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.RECIPIENT_MODAL)).not_to_be_visible()

    @allure.step("Заполняю поля сгенерированными данными")
    def fill_in_data(self):
        name_first = "вывЫвыв wdSdsdsdsd-вавава вававава'ывыывывывывывывывывывывывывывывыывывывывывыываывывывывв"
        # Генерация случайных первых трех букв кириллицы
        cyrillic_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        random_letters = ''.join(random.choices(cyrillic_letters, k=3))
        name = random_letters + name_first[3:]  # Замена первых трех символов
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        email = fake.email()

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)
        self.page.locator(self.EMAIL_FIELD).fill(email)

        return name, phone, email

    @allure.step("Заполняю поля сгенерированными данными")
    def fill_in_data_randomize(self):
        name = fake.name()
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        email = fake.email()

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)
        self.page.locator(self.EMAIL_FIELD).fill(email)

        return name, phone, email

    @allure.step("Заполняю поля сгенерированными данными")
    def fill_in_part_of_data_randomize(self):
        name = fake.name()
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)

        return name, phone

    @allure.step("Сохраняю отредактированного получателя")
    def save_edited_recipient(self):
        self.page.locator(self.SAVE_RECIPIENT_BUTTON).click()
        with allure.step("Проверяю, что модальное окно нового пользователя закрыто"):
            expect(self.page.locator(self.RECIPIENT_MODAL)).not_to_be_visible()
        with allure.step("Проверяю, что листинг пользователей закрыт"):
            expect(self.page.locator(self.recipient_listing.RECIPIENT_LISTING_MODAL)).not_to_be_visible()

    @allure.step("Сохраняю email")
    def save_email(self):
        email_selector = 'input[type="email"]'
        email_element = self.page.locator(email_selector)
        email_value = email_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")
        return email_value


"""Модалка подтверждения удаления"""


class DeleteConformationModal:

    DELETE_CONFIRMATION_MODAL = "p:has-text('Вы уверены, что хотите удалить получателя?')"
    CONFIRM_DELETE_BUTTON = "div.RecipientSelectionConfirm__Buttons span:has-text('Удалить')"
    CANCEL_DELETE_BUTTON = "div.RecipientSelectionConfirm__Buttons span:has-text('Отмена')"

    def __init__(self, page):
        self.recipient_listing = RecipientListing(page)
        self.adress_listing = AdressListing(page)
        self.obtaining_block = ObtainingBlock(page)
        self.page = page

    @allure.step("Подтвреждаю удаление")
    def delete_confirm(self):
        self.page.locator(self.CONFIRM_DELETE_BUTTON).click()
        with allure.step("Проверяю, что окно подтверждения удаления не отображается на странице"):
            expect(self.page.locator(self.DELETE_CONFIRMATION_MODAL)).not_to_be_visible()

    @allure.step("Отменяю удаление")
    def cancel_deletion(self):
        self.page.locator(self.CANCEL_DELETE_BUTTON).click()
        with allure.step("Проверяю, что окно подтверждения удаления не отображается на странице"):
            expect(self.page.locator(self.DELETE_CONFIRMATION_MODAL)).not_to_be_visible()

    @allure.step("Удаляю получателя")
    def delete_recipient_true(self):
        self.recipient_listing.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.recipient_listing.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.recipient_listing.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.recipient_listing.INFO_DESCRIPTION).inner_text()

        self.delete_confirm()
        self.recipient_listing.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

        for title in recipient_titles:
            assert title != actual_title, f"Найдено совпадение с эталонным значением: {title}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.recipient_listing.INFO_DESCRIPTION).all_text_contents()

        for description in recipient_descriptions:
            assert description != actual_description, f"Найдено совпадение с эталонным значением: {description}"

    @allure.step("Удаляю получателя")
    def delete_recipient(self):
        self.recipient_listing.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.recipient_listing.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Считаю количество записей в листинге(до удаления)"):
            recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

            number_of_records_before_deleting = 0
            for title in recipient_titles:
                number_of_records_before_deleting += 1
            print(number_of_records_before_deleting)

            self.delete_confirm()
            self.recipient_listing.open_recipient_listing()

        with allure.step("Считаю количество записей в листинге(после удаления)"):
            recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

            number_of_records_after_deleting = 0
            for title in recipient_titles:
                number_of_records_after_deleting += 1
            print(number_of_records_after_deleting)

        with allure.step("Проверяю, что запись была удалена"):
            assert number_of_records_before_deleting == number_of_records_after_deleting + 1

    @allure.step("Удаляю адрес")
    def delete_adress(self):
        self.adress_listing.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.adress_listing.CHECKED_ADRESS_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Считаю количество записей в листинге(до удаления)"):
            adress_titles = self.page.locator(self.adress_listing.INFO_TITLE).all_text_contents()

            number_of_records_before_deleting = 0
            for title in adress_titles:
                number_of_records_before_deleting += 1
            print(number_of_records_before_deleting)

            self.delete_confirm()
            self.obtaining_block.adress_listing_activation()

        with allure.step("Считаю количество записей в листинге(после удаления)"):
            adress_titles = self.page.locator(self.adress_listing.INFO_TITLE).all_text_contents()

            number_of_records_after_deleting = 0
            for title in adress_titles:
                number_of_records_after_deleting += 1
            print(number_of_records_after_deleting)

        with allure.step("Проверяю, что запись была удалена"):
            assert number_of_records_before_deleting == number_of_records_after_deleting + 1

    @allure.step("Отменяю удаление")
    def cancel_recipient_deletion(self):
        self.recipient_listing.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.recipient_listing.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.recipient_listing.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.recipient_listing.INFO_DESCRIPTION).inner_text()

        self.cancel_deletion()
        self.recipient_listing.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.recipient_listing.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"

    @allure.step("Закрываю окно удаления")
    def close_recipient_deletion_modal(self):
        self.recipient_listing.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.recipient_listing.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.recipient_listing.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.recipient_listing.INFO_DESCRIPTION).inner_text()

        self.page.mouse.click(0, 0)
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.CONFIRM_DELETE_BUTTON)).not_to_be_visible()

        self.recipient_listing.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.recipient_listing.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"


"""Блок Получение"""


class ObtainingBlock:

    ADD_FIRST_ADRESS_BUTTON = "#shipping .SectionInfo__ButtonAdd"
    CHANGE_BUTTON = "#shipping .SectionInfo__Button"
    ADRESS_INFO = "#shipping .CheckoutSection__Body span.SectionInfo__Title"
    TYPE_PICKUP_POINT = "#shipping .CheckoutSection__Body span.SectionInfo__Info"
    PICKUP_POINT_ADRESS = "#shipping .SectionInfo__Title"
    PICKUP_POINT_BUTTON = "button.CheckoutShippingControl__Button span:has-text('Пункт выдачи')"
    COURIER_BUTTON = "button.CheckoutShippingControl__Button span:has-text('Курьером')"

    def __init__(self, page):
        self.page = page
        self.adress_listing = AdressListing(page)

    @allure.step("Открываю листинг адресов")
    def adress_listing_activation(self):
        self.page.locator(self.CHANGE_BUTTON).click()

    # Локатор адреса ПВЗ в блоке Получение
    def pickup_point_adress(self):
        return self.page.locator(self.PICKUP_POINT_ADRESS)

    @allure.step("Открываю листинг адресов ПВЗ")
    def pickup_point_adress_listing_activation(self):
        self.page.locator(self.PICKUP_POINT_BUTTON).click()

    @allure.step("Открываю листинг адресов оставки курьером")
    def courier_adress_listing_activation(self):
        self.page.locator(self.COURIER_BUTTON).click()

    @allure.step("Запоминаю адрес в блоке Получение")
    def check_out_adress(self):
        return self.page.locator(self.ADRESS_INFO).inner_text()

    @allure.step("Запоминаю адрес в блоке Получение")
    def click_first_adress_button(self):
        return self.page.locator(self.ADD_FIRST_ADRESS_BUTTON).click()



    # @allure.step("Удвляб адрес")
    # def address_deletion(self):
    #     self.adress_listing.open_action_menu()
    #     self.delete_conformation_modal.delete_adress()


"""Листинг адресов"""


class AdressListing:

    ADRESS_LISTING_MODAL = ".AddressSelection .flexColumn.KitModal__Inner"
    ADD_ADRESS_BUTTON = "button.AddressSelection__ButtonAdd"
    ACTION_MENU = ".AddressSelection__ButtonEdit"
    ACTION_MENU_MODAL = ".AddressSelection__Item__Tooltip.--open-tooltip"
    EDIT_BUTTON = ".AddressSelection__Item__Tooltip.--open-tooltip span:has-text('Редактировать')"
    DELETE_BUTTON = ".AddressSelection__Item__Tooltip.--open-tooltip span:has-text('Удалить')"
    # CHANGE_RECIPIENT_MODAL = "p:has-text('Изменить получателя')"
    SELECTED_RADIO_BUTTON = "input[type='radio']:checked"
    UNSELECTED_RADIO_BUTTON = ".Radio__Inner >> input[type='radio']:not(:checked)"
    RECIPIENT_BLOCK = "li.AddressSelection__Item"
    INFO_TITLE = "p.AddressSelection__InfoTitle"
    INFO_DESCRIPTION = "p.AddressSelection__InfoDescription"
    CHECKED_ADRESS_BLOCK = "li.AddressSelection__Item:has(input[type='radio']:checked)"
    ADRESS_SELECTION_BUTTON = "button.AddressSelection__ButtonChange"
    DELETE_CONFIRMATION_MODAL = "p:has-text('Вы уверены, что хотите удалить адрес доставки?')"
    #TODO: нужны два локатора при нажатии на редактировать, убедится, что пункт выдачи кнопка выделена, курьер выделен при выделения курьера и полявились поля
    # CHANGE_ADRESS_MODAL = "p:has-text('Изменить получателя')"

    def __init__(self, page):
        self.page = page
        self.obtaining_block = ObtainingBlock
        self.adress_listing = AdressListing
        self.map = Map(page)

    @allure.step("Открываю листинг адресов")
    def adress_listing_modal(self):
        return self.page.locator(self.ADRESS_LISTING_MODAL)

    @allure.step("Выбираю ПВЗ по кастомному событию")
    def select_pickup_point(self, pickup_point_id: str, latitude: float, longitude: float):
        """
        Эмулирует выбор ПВЗ через кастомное событие.

        :param pickup_point_id: ID пункта выдачи.
        :param latitude: Широта пункта.
        :param longitude: Долгота пункта.
        """

        # Формируем и отправляем кастомное событие через evaluate
        self.page.evaluate(
            """
            ({pickup_point_id, latitude, longitude}) => {
                const element = document;
                const event = new CustomEvent('$yandex-map-centering', {
                    detail: {
                        id: pickup_point_id,
                        pickupPointId: pickup_point_id,
                        lat: latitude,
                        lon: longitude,
                        kind: "PICKUP_POINT",
                        brand: "CDEK"
                    }
                });
                element.dispatchEvent(event);
            }
            """,
            {
                "pickup_point_id": pickup_point_id,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    @allure.step("Открываю модалку Карты")
    def click_add_adress_button(self):
        return self.page.locator(self.ADD_ADRESS_BUTTON).click()

    @allure.step("ереключаю на неактивный адрес")
    def switch_on_inactive_adress(self):
        # Локатор для первого невыбранного радио-баттона
        radio_locator = self.page.locator(self.UNSELECTED_RADIO_BUTTON).nth(0)

        # Клик по соседнему span.Radio__Button
        radio_locator.locator("xpath=..").locator("span.Radio__Button").click()

    @allure.step("Выбираю неактивный адрес")
    def select_inactive_adress(self):
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_ADRESS_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()
            actual_info_listing = f"{actual_title}, {actual_description}"

        with allure.step("Нажимаю кнопку Выбрать"):
            self.page.locator(self.ADRESS_SELECTION_BUTTON).click()

        with allure.step("Извлекаю текст из блока Получение"):
            actual_type_check_out = self.page.locator(self.obtaining_block.TYPE_PICKUP_POINT).inner_text()
            actual_type_check_out = actual_type_check_out.replace(':', '')
            actual_description_check_out = self.page.locator(self.obtaining_block.ADRESS_INFO).inner_text()
            actual_info_check_out = f"{actual_type_check_out}, {actual_description_check_out}"

        with allure.step("Сравниваю информацию в блоке Получние с адресом выбранным в листинге "):
            assert actual_info_check_out.lower() == actual_info_listing.lower(), f"Expected '{actual_info_listing}', but got '{actual_info_check_out}'"

    @allure.step("Открываю экшн меню")
    def open_action_menu(self):
        with allure.step("Нахожу блок с активной радиокнопкой"):
            parent_block = self.page.locator(self.CHECKED_ADRESS_BLOCK)

            if parent_block.count() > 0:  # Проверяем, есть ли активный блок
                with allure.step("Нажимаю на экшн меню в активном блоке"):
                    parent_block.locator(self.ACTION_MENU).click()
            else:
                with allure.step("Блок с активной радиокнопкой не найден, выбираю первый невыбранный"):
                    parent_block = self.page.locator(self.UNSELECTED_RADIO_BUTTON).first.locator("xpath=ancestor::li")
                    with allure.step("Нажимаю на экшн меню в новом выбранном блоке"):
                        parent_block.locator(self.ACTION_MENU).click()

        # self.page.locator(self.ACTION_MENU).nth(0).click()
        with allure.step("Проверяю, что экшн меню открыто"):
            expect(self.page.locator(self.ACTION_MENU_MODAL)).to_be_enabled()
        with allure.step("Проверяю, что в меню отображаются кнопки Редактировать и Удалить"):
            expect(self.page.locator(self.EDIT_BUTTON)).to_be_visible()
            expect(self.page.locator(self.DELETE_BUTTON)).to_be_visible()

    @allure.step("Нажимаю на Редактировать")
    def click_edit_button(self):
        self.page.locator(self.EDIT_BUTTON).click()

    @allure.step("Нажимаю на Удалить")
    def click_delete_button(self):
        self.page.locator(self.DELETE_BUTTON).click()
        with allure.step("Проверяю, что окно подтверждения удаления отображается на странице"):
            expect(self.page.locator(self.DELETE_CONFIRMATION_MODAL)).to_be_visible()


    #TODO доделать
    @allure.step(
        "Проверяю, что новый адрес появился в листинге, его информация соответствует заданной, он активен")
    def verify_selected_adress_info(self, expected_description): #Добавить expected_title если будем проверять тип точки
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_ADRESS_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            # actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        with allure.step("Сравниваю с ожидаемыми значениями"):
            # assert actual_title.lower() == expected_title.lower(), f"Ожидалось: {expected_title}, Получено: {actual_title}"
            assert actual_description == expected_description, f"Ожидалось: {expected_description}, Получено: {actual_description}"

    @allure.step("Проверяю, что все адреса являются ПВЗ")
    def check_all_pickup_points(self):
        adress_titles = self.page.locator(self.adress_listing.INFO_TITLE).all_text_contents()
        assert all(re.search('Пункт выдачи', title) for title in adress_titles), \
            f"{'Пункт выдачи'} не найден в списке: {adress_titles}"

    @allure.step("Проверяю, что все адреса являются адресами для курьера")
    def check_all_courier_adress(self):
        adress_titles = self.page.locator(self.adress_listing.INFO_TITLE).all_text_contents()
        assert all(re.search('Доставка по адресу', title) for title in adress_titles), \
            f"{'Доставка по адресу'} не найдена в списке: {adress_titles}"

    @allure.step("Запоминаю выбранный адрес в листинге адресов")
    def get_selected_adress_info(self): #Добавить expected_title если будем проверять тип точки
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_ADRESS_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            # actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            return parent_block.locator(self.INFO_DESCRIPTION).inner_text()




"""Модальное окно Карты"""


class Map:

    MAP_MODAL = "h2:has-text('Способ доставки')"
    PICKUP_POINT_BUTTON = "button.CheckoutChooseMethod__Button span:has-text('Пункт выдачи')"
    COURIER_ADRESS_BUTTON = "button.CheckoutChooseMethod__Button span:has-text('Курьером')"
    PICK_UP_HERE_BUTTON = "button.ShippingForm__Choose"
    PICKUP_POINT_ADRESS = ".ShippingStoreCard__Description"
    PICKUP_POINT_CARD_INFO = "div.ShippingStoreCard"
    COURIER_BUTTON = ".CheckoutChooseMethod button span:has-text('Курьером')"
    ADRESS_TEXTAREA = "textarea[placeholder='Адрес']"
    APARTMENT_INPUT = "input[placeholder='Квартира']"
    ENTRYWAY_INPUT = "input[placeholder='Подъезд']"
    FLOOR_INPUT = "input[placeholder='Этаж']"
    INTERCOM_INPUT = "input[placeholder='Домофон']"
    COMMENTARY_TEXTAREA = "textarea[placeholder='Комментарий']"
    ADRESS_IN_ADRESS_LIST = "button.CheckoutAddressPoint__Overlay"
    TEXT_FROM_ADRESS_IN_ADRESS_LIST = "div.CheckoutAddressPoint p"
    BACK_BUTTON = "button.CheckoutButtonPrev"
    CONTROL_PANEL = "div.CheckoutChooseMethod"

    def __init__(self, page):
        self.page = page
        self.buyer_and_recipient_block = BuyerAndRecipientBlock

    @allure.step("Открываю Карту")
    def map_modal(self):
        return self.page.locator(self.MAP_MODAL)

    # Метод ля вызова самой кнопки "Пункт выдачи"
    def pickup_point_button(self):
        return self.page.locator(self.PICKUP_POINT_BUTTON)

    # Та часть элемента где хранится статус "Выбран"
    def pickup_point_button_status(self):
        return self.page.locator(self.PICKUP_POINT_BUTTON).locator('xpath=ancestor::button')

    def courier_button_status(self):
        return self.page.locator(self.COURIER_ADRESS_BUTTON).locator('xpath=ancestor::button')

    def adress_textaria_status(self):
        return self.page.locator(self.ADRESS_TEXTAREA)

    def type_in_textaria(self, text):
        return self.page.locator(self.ADRESS_TEXTAREA).fill(text)

    @allure.step("Заполняю дополнительные поля")
    def filling_in_additional_fields(self):
        # Заполняем поля
        aprtment = str(random.randint(1, 999))
        entryway = str(random.randint(1, 20))
        floor = str(random.randint(1, 20))
        intercom = str(random.randint(100, 999))
        commentary = "Прошу позвонить, за 10 мин до приезда"

        self.page.locator(self.APARTMENT_INPUT).fill(aprtment)
        self.page.locator(self.ENTRYWAY_INPUT).fill(entryway)
        self.page.locator(self.FLOOR_INPUT).fill(floor)
        self.page.locator(self.INTERCOM_INPUT).fill(intercom)
        self.page.locator(self.COMMENTARY_TEXTAREA).fill(commentary)

        return aprtment, entryway, floor, intercom, commentary

    @allure.step("Открываю Карту")
    def pickup_point_button(self):
        return self.page.locator(self.PICKUP_POINT_BUTTON)

    @allure.step("Открываю Карту")
    def pick_up_here_button(self):
        return self.page.locator(self.PICK_UP_HERE_BUTTON)

    @allure.step("Подтверждаю выбор ПВЗ")
    def click_pick_up_here_button(self):
        return self.page.locator(self.PICK_UP_HERE_BUTTON).click()

    @allure.step("Выбираю доставку курьером")
    def click_courier_button(self):
        return self.page.locator(self.COURIER_BUTTON).click()

    # Локатор адреса ПВЗ в модалке Карты
    def pickup_point_adress(self):
        return self.page.locator(self.PICKUP_POINT_ADRESS)

    @allure.step("Открываю Карту")
    def pickup_point_card_info(self):
        return self.page.locator(self.PICKUP_POINT_CARD_INFO)

    @allure.step("Выбираю первый адрес в списке")
    def click_first_adress_in_list(self):
        return self.page.locator(self.ADRESS_IN_ADRESS_LIST).first.click()

    @allure.step("Выбираю первый адрес в списке")
    def text_from_first_adress_in_list(self):
        return self.page.locator(self.TEXT_FROM_ADRESS_IN_ADRESS_LIST).first

    @allure.step("Нажимаю кнопку Назад")
    def click_back_button(self):
        return self.page.locator(self.BACK_BUTTON).click()

    # Панель контроля (ПУНКТ ВЫДАЧИ, КУРЬЕРОМ)
    def control_panel(self):
        return self.page.locator(self.CONTROL_PANEL)

    @allure.step("Запоминаю данные с дополнительных полях")
    def get_additional_fields_info(self):
        aprtment_element = self.page.locator(self.APARTMENT_INPUT)
        aprtment = aprtment_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")
        entryway_element = self.page.locator(self.ENTRYWAY_INPUT)
        entryway = entryway_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")
        floor_element = self.page.locator(self.FLOOR_INPUT)
        floor = floor_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")
        intercom_element = self.page.locator(self.INTERCOM_INPUT)
        intercom = intercom_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")
        commentary_element = self.page.locator(self.COMMENTARY_TEXTAREA)
        commentary = commentary_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")

        return aprtment, entryway, floor, intercom, commentary




"""Блок Доставка"""


class DeliveryBlock:

    PRODUCT_PRICE = "p.CheckoutDeliveryProduct__Price"

    def __init__(self, page):
        self.page = page

    @allure.step("Запоминаю первоначальную стоимость товара")
    def base_price(self):
        text_base_price = self.page.locator(self.PRODUCT_PRICE).inner_text()
        base_price_number = float(text_base_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽/шт.', ''))
        return base_price_number


"""Блок Калькуляции"""


class CalculationBlock:

    def __init__(self, page):
        self.page = page


    # @allure.step("Запоминаю стоимость скидки")
    # def discounted_price(self):
    #     text_discounted_price = self.page.locator(self.PRODUCT_PRICE_DISCOUNTED).inner_text()
    #     discounted_price_number = float(text_discounted_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.'))
    #     return discounted_price_number


""" Блок 'Промокод' """


class PromoCode:

    PROMO_CODE_FIELD_INFO = ".Field__Info .Field__Text"
    CLEAR_PROMO_CODE_FIELD_BUTTON = ".flexRow-C.FieldControls__Button.active"
    PROMO_CODE_FIELD = ".kit-input.Field__Input.disable-label"
    PROMO_CODE_FIELD_CHECK = ".Field.PromoWidget__Field.is-small.has-controls"
    PROMO_CODE_HINT_ICON = "div.Tooltip__Icon"
    PROMO_CODE_HINT_POPUP = ".Tooltip__Inner.v-enter-to .Tooltip__Content"
    CANCEL_PROMO_CODE_BUTTON = ".flexRow-AIC.PromoWidget__CancelButton"
    PROMO_CODE_TOGGLE_BUTTON = ".PromoWidget__ToggleButton"
    PROMO_CODE_APPLY_BUTTON = ".PromoWidget__SubmitButton.Button.size--normal.color--secondary"

    def __init__(self, page):
        self.page = page

    @allure.step("Активирую валидный промокод")
    def price_changes_with_a_promo_code(self):
        self.open_promo_code_bar()
        self.check_promo_code()

    @allure.step("Отменяю промокод если он был установлен")
    def check_promo_code(self):
        self.open_promo_code_bar()
        if self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).is_visible():
            self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).click()
        else:
            return
            # self.fill_valid_promo_code()
            # self.click_apply_button()

    @allure.step("Открываю блок 'Промокод'")
    def open_promo_code_bar(self):
        self.page.locator(self.PROMO_CODE_TOGGLE_BUTTON).click()

    @allure.step("Закрываю блок 'Промокод'")
    def close_promo_code_bar(self):
        self.open_promo_code_bar()

    # Открытие/закрытие блока промокод
    def promo_code_bar(self):
        return self.page.locator(self.PROMO_CODE_TOGGLE_BUTTON)

    @allure.step("Ввожу валидный промокод")
    def fill_valid_promo_code(self):
        self.page.locator(self.PROMO_CODE_FIELD).fill("НАЧАЛО")

    @allure.step("Ввожу невалидный промокод")
    def fill_invalid_promo_code(self):
        self.page.locator(self.PROMO_CODE_FIELD).fill("12345DF")

    @allure.step("Нажимаю 'Применить'")
    def click_apply_button(self):
        self.page.locator(self.PROMO_CODE_APPLY_BUTTON).click()

    # Версия активации когда не нужно запоминать цену
    # @allure.step("Активирую валидный промокод")
    # def activate_valid_promo_code(self):
    #     self.open_promo_code_bar()
    #     self.check_promo_code()
    #     self.fill_valid_promo_code()
    #     self.click_apply_button()

    @allure.step("Активирую валидный промокод")
    def activate_valid_promo_code(self):
        self.fill_valid_promo_code()
        self.click_apply_button()

    @allure.step("Активирую невалидный промокод")
    def activate_invalid_promo_code(self):
        # self.open_promo_code_bar()
        self.fill_invalid_promo_code()
        self.click_apply_button()

    # Подсказка поля промокод
    def promo_code_field_info(self):
        return self.page.locator(self.PROMO_CODE_FIELD_INFO)

    @allure.step("Отменяю примененный промокод")
    def cancel_promo_code(self):
        self.page.locator(self.CANCEL_PROMO_CODE_BUTTON).click()

    @allure.step("Очищаю поле Промокод нажатием на крестик")
    def clear_promo_code_field_by_cross(self):
        self.page.locator(self.CLEAR_PROMO_CODE_FIELD_BUTTON).click()

    # Поле промокод
    def promo_code_field(self):
        return self.page.locator(self.PROMO_CODE_FIELD_CHECK)

    @allure.step("Навожу курсор на подсказку")
    def hover_to_promo_code_hint(self):
        self.page.locator(self.PROMO_CODE_HINT_ICON).hover()

    # Подсказка
    def promo_code_hint_popup(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP)

    # Текст подсказки
    def promo_code_hint_popup_text(self):
        return self.page.locator(self.PROMO_CODE_HINT_POPUP).inner_text()







#
# page-url: https://garwin.ru/checkout
# pointer-click: rn:710765266:x:32504:y:23772:t:85958:p:****AAA3AAAA1A1AA1A2AA1AA2AA1A1:X:1167:Y:246
# browser-info: u:1734619901805257952:v:1551:vf:14pwap7gbnncs44tf8xglmzmdcdb:rqnl:1:st:1736765012
# t: gdpr(14)ti(1)

