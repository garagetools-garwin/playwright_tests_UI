import random
import allure
import re
import time
from faker import Faker
from playwright.sync_api import expect, Page

fake = Faker('ru_RU')


class CheckoutPage:

    PATH = "/checkout"

    ORDER_BUTTON = ".OrderTotal__Button.Button.size--medium.color--primary"
    LOGO_BUTTON = ".Logotype.nuxt-link-active"

    def __init__(self, page: Page):
        self.page = page

        self.buyer_and_recipient_block = BuyerAndRecipientBlock(page)
        self.buyer_listing = BuyerListing(page)
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
        self.payment_block = PaymentBlock(page)
        self.commentary_block = CommentaryBlock(page)

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    def click_logo_button(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.locator(self.LOGO_BUTTON).click()



"""Блок Покупатель и получатель"""


class BuyerAndRecipientBlock:

    ADD_FIRST_RECIPIENT_BUTTON = "#shipping .CheckoutSection__Footer .SectionInfo__ButtonAdd" #TODO перенести в блок получения
    RECIPIENT_CHANGE_BUTTON = "#shipping .CheckoutSection__Footer .SectionInfo__Button" #TODO перенести в блок получения
    BYUER_CHANGE_BUTTON = "#contacts .CheckoutSection__Custom .SectionInfo__Button"
    CUSTOMER_NAME = "#contacts .CheckoutSection__Custom span.SectionInfo__Title"
    RECIPIENT_INFO = "#shipping .CheckoutSection__Footer span.SectionInfo__Title" #TODO перенести в блок получения

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открываю окно Нового получателя")
    def click_add_first_recipient_button(self):
        self.page.locator(self.ADD_FIRST_RECIPIENT_BUTTON).wait_for(timeout=3000)
        self.page.locator(self.ADD_FIRST_RECIPIENT_BUTTON).click()


    @allure.step("Создаю нового получателя")
    def create_recipient(self, base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        recipient_listing_opened = False

        # Попытка открыть список получателей
        try:
            checkout_page.recipient_listing.open_recipient_listing()
            recipient_listing_opened = True
        except Exception:
            pass  # Игнорируем ошибку, продолжаем

        # Попытка нажать кнопку "Добавить первого получателя"
        if not recipient_listing_opened:  # Только если предыдущее действие не сработало
            try:
                checkout_page.buyer_and_recipient_block.click_add_first_recipient_button()
                recipient_listing_opened = True
            except Exception:
                pass  # Игнорируем ошибку, продолжаем

        # Если хотя бы одно из действий сработало, продолжаем
        if recipient_listing_opened:
            checkout_page.add_recipient_modal.add_recipient_modal_open()
            with allure.step(
                    "Ввожу текст в котором включены все допустимые буквы и символы, их максимальное количество"):
                name, phone, email = checkout_page.add_recipient_modal.fill_in_data()
            checkout_page.add_recipient_modal.click_save_new_recipient_button()
            with allure.step("Формирую ожидаемый текст"):
                expected_info = f"{name}, {email}, {phone}"
            checkout_page.add_recipient_modal.verify_recipient_info(expected_info)
            checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

            with allure.step("Формирую ожидаемый текст"):
                expected_info_title = name
                expected_info_description = f"{email}, {phone}"
            with allure.step("Проверяю информацию о выбранном получателе"):
                checkout_page.add_recipient_modal.verify_selected_recipient_info(expected_info_title,
                                                                                 expected_info_description)
                checkout_page.recipient_listing.close_recipient_listing()

            return name, email, phone

        # Текст имени получателя
    def customer_name_text(self):
        return self.page.locator(self.CUSTOMER_NAME).inner_text()


"""Листинг покупателей"""


class BuyerListing:

    BUYER_LISTING_MODAL = ".ContextSelection .flexColumn.KitModal__Inner"
    SELECTED_RADIO_BUTTON = "input[type='radio']:checked"
    UNSELECTED_RADIO_BUTTON = ".Radio__Inner >> input[type='radio']:not(:checked)"
    SPECIFIC_CUSTOMER = 'li#delivery-point:has(.ContextSelection__InfoTitle:has-text("ООО \\"У КУПЦА\\"")) label'
    BUYER_BLOCK = "#delivery-point"
    INFO_TITLE = ".ContextSelection__InfoTitle"
    CHECKED_BUYER_BLOCK = "li#delivery-point:has(input[type='radio']:checked)"
    BUYER_SELECTION_BUTTON = "button.ContextSelection__ButtonChange"
    CLOSE_BUTTON = ".ContextSelection .KitModal__Closer"

    def __init__(self, page: Page):
        self.page = page
        self.buyer_and_recipient_block = BuyerAndRecipientBlock

    @allure.step("Открываю листинг покупателей")
    def buyer_listing(self):
        return self.page.locator(self.BUYER_LISTING_MODAL)

    @allure.step("Закрываю модальное окно листинга покупателей")
    def close_buyer_listing_modal1(self):
        self.page.locator(self.CLOSE_BUTTON).click()
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.BUYER_LISTING_MODAL)).not_to_be_visible()

    @allure.step("Закрываю модальное окно листинга покупателей")
    def close_buyer_listing_modal2(self):
        self.page.mouse.click(0, 0)
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.BUYER_LISTING_MODAL)).not_to_be_visible()

    @allure.step("Открываю листинг покупателей")
    def open_buyer_listing(self):
        # Ожидаем появления кнопки в течение 3 секунд
        self.page.locator(self.buyer_and_recipient_block.BYUER_CHANGE_BUTTON).wait_for(timeout=3000)
        self.page.locator(self.buyer_and_recipient_block.BYUER_CHANGE_BUTTON).click()

    @allure.step("Переключаюсь на неактивного покупателя")
    def switch_on_inactive_buyer(self):
        # Локатор для первого невыбранного радио-баттона
        radio_locator = self.page.locator(self.UNSELECTED_RADIO_BUTTON).nth(0)

        # Клик по соседнему span.Radio__Button
        radio_locator.locator("xpath=..").locator("span.Radio__Button").click()

    @allure.step("Переключаюсь на конкретного покупателя")
    def switch_a_specific_customer(self):
        locator = self.page.locator(self.SPECIFIC_CUSTOMER)
        locator.click()

    @allure.step("Выбираю неактивного покупателя")
    def select_inactive_buyer(self):
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_BUYER_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_info_listing = parent_block.locator(self.INFO_TITLE).inner_text()
            print(actual_info_listing)

        with allure.step("Нажимаю кнопку Выбрать"):
            self.page.locator(self.BUYER_SELECTION_BUTTON).click()

        with allure.step("Извлекаю текст из блока Покупатель"):
            time.sleep(1)
            actual_info_check_out = self.page.locator(self.buyer_and_recipient_block.CUSTOMER_NAME).inner_text()
            print(actual_info_check_out)

        with allure.step("Сравниваю информацию в блоке Покупатель с покупателем выбранным в листинге "):
            assert actual_info_check_out.lower() == actual_info_listing.lower(), f"Expected '{actual_info_listing}', but got '{actual_info_check_out}'"


    @allure.step("Считаю количество записей в листинге")
    def counting_the_number_of_customers(self):
        count_of_customers = self.page.locator(self.BUYER_BLOCK).count()
        print(count_of_customers)
        return count_of_customers

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
    CLOSE_BUTTON = ".RecipientSelection .KitModal__Closer"

    def __init__(self, page: Page):
        self.page = page
        self.buyer_and_recipient_block = BuyerAndRecipientBlock

    @allure.step("Извлекаю ФИО первого получателя")
    def name_of_first_recipient(self):
        return self.page.locator(self.INFO_TITLE).nth(0).inner_text()

    @allure.step("Извлекаю телефон и адресс почты первого получателя")
    def phone_and_email_of_first_recipient(self):
        return self.page.locator(self.INFO_DESCRIPTION).nth(0).inner_text()

    @allure.step("Открываю листинг получателей")
    def open_recipient_listing(self):
        # Ожидаем появления кнопки в течение 3 секунд
        self.page.locator(self.buyer_and_recipient_block.RECIPIENT_CHANGE_BUTTON).wait_for(timeout=3000)
        self.page.locator(self.buyer_and_recipient_block.RECIPIENT_CHANGE_BUTTON).click()

        # Проверяем, действительно ли открылся листинг
        with allure.step("Проверяю, что листинг пользователей открыт"):
            expect(self.page.locator(self.RECIPIENT_LISTING_MODAL)).to_be_visible(timeout=3000)

    def recipient_listing_modal(self):
        return self.page.locator(self.RECIPIENT_LISTING_MODAL)

    @allure.step("Открываю листинг получателей")
    def open_recipient_listing_try(self, base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        recipient_listing_opened = False

        # Попытка открыть список получателей
        try:
            checkout_page.recipient_listing.open_recipient_listing()
            recipient_listing_opened = True
        except Exception:
            pass  # Игнорируем ошибку, продолжаем

        # Попытка нажать кнопку "Добавить первого получателя"
        if not recipient_listing_opened:  # Только если предыдущее действие не сработало
            try:
                checkout_page.buyer_and_recipient_block.click_add_first_recipient_button()
                recipient_listing_opened = True
            except Exception:
                pass  # Игнорируем ошибку, продолжаем

        # Если хотя бы одно из действий сработало, продолжаем
        if recipient_listing_opened:
            pass

    @allure.step("Переключаюсь на неактивного получателя")
    def switch_on_inactive_recipient(self):
        # Локатор для первого невыбранного радио-баттона
        radio_locator = self.page.locator(self.UNSELECTED_RADIO_BUTTON).nth(0)

        # Клик по соседнему span.Radio__Button
        radio_locator.locator("xpath=..").locator("span.Radio__Button").click()

    @allure.step("Выбираю неактивного получателя")
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

    @allure.step("Закрываю листинг получателей")
    def close_recipient_listing(self):
        if self.page.locator(self.RECIPIENT_LISTING_MODAL).is_visible():
            self.page.locator(self.CLOSE_BUTTON).click()
        else:
            pass

    @allure.step("Считаю количество записей в листинге")
    def count_number_of_records(self):
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        number_of_records = 0
        for title in recipient_titles:
            number_of_records += 1
        print(number_of_records)
        return number_of_records


"""Модалка Новый получатель"""


class AddRecipientModal:

    RECIPIENT_MODAL = ".RecipientSelectionAdd .flexColumn.KitModal__Inner"
    NAME_FIELD = "div.RecipientSelectionAdd__Input input[type='text']"
    TEL_FIELD = "div.RecipientSelectionAdd__Input input[type='tel']"
    EMAIL_FIELD = "div.RecipientSelectionAdd__Input input[type='email']"
    SAVE_RECIPIENT_BUTTON = "button.RecipientSelectionAdd__Button"
    CLOSE_BUTTON = ".RecipientSelectionAdd .KitModal__Closer"
    FIELD_ERROR_TEXT = ".Field.RecipientSelectionAdd__Input .Field__Text"

    def __init__(self, page: Page):
        self.page = page
        self.recipient_listing = RecipientListing
        self.add_recipient_modal = AddRecipientModal
        self.buyer_and_recipient_block = BuyerAndRecipientBlock

    # Модальное окно нового получателя
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
    def fill_in_name_and_phone_data_randomize(self):
        name = fake.name()
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)

        return name, phone

    @allure.step("Заполняю поле ФИО сгенерированными данными")
    def fill_name_data_randomize(self):
        name = fake.name().replace('.', '')
        self.page.locator(self.NAME_FIELD).fill(name)

        return name

    @allure.step("Заполняю поле Телефон сгенерированными данными")
    def fill_phone_data_randomize(self):
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        self.page.locator(self.TEL_FIELD).fill(phone)

        return phone

    @allure.step("Заполняю поле e-mail сгенерированными данными")
    def fill_email_data_randomize(self):
        email = fake.email()

        self.page.locator(self.EMAIL_FIELD).fill(email)

        return email

    @allure.step("Заполняю поле ФИО данными заданными в ручную")
    def fill_name(self, text):
        self.page.locator(self.NAME_FIELD).fill(text)

        # return text

    @allure.step("Заполняю поле Телефон данными заданными в ручную")
    def fill_phone(self, text):
        self.page.locator(self.TEL_FIELD).fill(text)

        # return phone

    @allure.step("Заполняю поле e-mail данными заданными в ручную")
    def fill_email(self, text):
        self.page.locator(self.EMAIL_FIELD).fill(text)

        # return email

    @allure.step("Очищаю все поля")
    def clear_all_fields(self):
        self.page.locator(self.NAME_FIELD).fill("")
        self.page.locator(self.TEL_FIELD).fill("")
        self.page.locator(self.EMAIL_FIELD).fill("")

    @allure.step("Получаю текст ошибки поля ФИО")
    def name_field_error_text(self):
        return self.page.locator(self.FIELD_ERROR_TEXT).nth(0).inner_text()

    @allure.step("Получаю текст ошибки поля Телефон")
    def phone_field_error_text(self):
        return self.page.locator(self.FIELD_ERROR_TEXT).nth(1).inner_text()

    @allure.step("Получаю текст ошибки поля email")
    def email_field_error_text(self):
        return self.page.locator(self.FIELD_ERROR_TEXT).nth(2).inner_text()


    @allure.step("Нажимаю на кнопку Сохранить")
    def click_save_new_recipient_button(self):
        self.page.locator(self.SAVE_RECIPIENT_BUTTON).click()

    @allure.step("Открываю окно Новый получатель")
    def add_recipient_modal_open(self):
        self.page.locator(self.recipient_listing.ADD_RECIPIENT_BUTTON).click()
        with allure.step("Проверяю, что модальное окно нового получателя открыто"):
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




"""Модалка Изменить получателя"""


class EditRecipientModal:

    RECIPIENT_MODAL = ".RecipientSelectionEdit .flexColumn.KitModal__Inner"
    NAME_FIELD = "div.RecipientSelectionEdit__Input input[type='text']"
    TEL_FIELD = "div.RecipientSelectionEdit__Input input[type='tel']"
    EMAIL_FIELD = "div.RecipientSelectionEdit__Input input[type='email']"
    SAVE_RECIPIENT_BUTTON = "button.RecipientSelectionEdit__Button"
    CLOSE_BUTTON = ".RecipientSelectionEdit .KitModal__Closer"
    FIELD_ERROR_TEXT = ".Field.RecipientSelectionEdit__Input .Field__Text"

    def __init__(self, page: Page):
        self.page = page
        self.recipient_listing = RecipientListing

    def edit_recipient_modal(self):
        return self.page.locator(self.RECIPIENT_MODAL)

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
    def fill_in_name_and_phone_data_randomize(self):
        name = fake.name()
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        self.page.locator(self.NAME_FIELD).fill(name)
        self.page.locator(self.TEL_FIELD).fill(phone)

        return name, phone

    @allure.step("Нажимаю на Сохранить")
    def click_save_edited_recipient_button(self):
        self.page.locator(self.SAVE_RECIPIENT_BUTTON).click()

    @allure.step("Сохраняю email")
    def save_email(self):
        email_selector = 'input[type="email"]'
        email_element = self.page.locator(email_selector)
        email_value = email_element.evaluate("(el) => el.shadowRoot ? el.shadowRoot.value : el.value")
        return email_value

    @allure.step("Заполняю поле ФИО сгенерированными данными")
    def fill_name_data_randomize(self):
        name = fake.name().replace('.', '')
        self.page.locator(self.NAME_FIELD).fill(name)

        return name

    @allure.step("Заполняю поле Телефон сгенерированными данными")
    def fill_phone_data_randomize(self):
        phone = f"+7 ({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

        self.page.locator(self.TEL_FIELD).fill(phone)

        return phone

    @allure.step("Заполняю поле e-mail сгенерированными данными")
    def fill_email_data_randomize(self):
        email = fake.email()

        self.page.locator(self.EMAIL_FIELD).fill(email)

        return email

    @allure.step("Заполняю поле ФИО данными заданными в ручную")
    def fill_name(self, text):
        self.page.locator(self.NAME_FIELD).fill(text)

        # return text

    @allure.step("Заполняю поле Телефон данными заданными в ручную")
    def fill_phone(self, text):
        self.page.locator(self.TEL_FIELD).fill(text)

        # return phone

    @allure.step("Заполняю поле e-mail данными заданными в ручную")
    def fill_email(self, text):
        self.page.locator(self.EMAIL_FIELD).fill(text)

        # return email

    @allure.step("Очищаю все поля")
    def clear_all_fields(self):
        self.page.locator(self.NAME_FIELD).fill("")
        self.page.locator(self.TEL_FIELD).fill("")
        self.page.locator(self.EMAIL_FIELD).fill("")

    @allure.step("Получаю текст ошибки поля ФИО")
    def name_field_error_text(self):
        return self.page.locator(self.FIELD_ERROR_TEXT).nth(0).inner_text()

    @allure.step("Получаю текст ошибки поля Телефон")
    def phone_field_error_text(self):
        return self.page.locator(self.FIELD_ERROR_TEXT).nth(1).inner_text()

    @allure.step("Получаю текст ошибки поля email")
    def email_field_error_text(self):
        return self.page.locator(self.FIELD_ERROR_TEXT).nth(2).inner_text()


"""Модалка подтверждения удаления"""


class DeleteConformationModal:

    DELETE_CONFIRMATION_MODAL = "p:has-text('Вы уверены, что хотите удалить получателя?')"
    CONFIRM_DELETE_BUTTON = "div.RecipientSelectionConfirm__Buttons span:has-text('Удалить')"
    CANCEL_DELETE_BUTTON = "div.RecipientSelectionConfirm__Buttons span:has-text('Отмена')"

    def __init__(self, page: Page):
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
    def delete_recipient_true(self, base_url, page_fixture):
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
        self.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

        for title in recipient_titles:
            assert title != actual_title, f"Найдено совпадение с эталонным значением: {title}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.recipient_listing.INFO_DESCRIPTION).all_text_contents()

        for description in recipient_descriptions:
            assert description != actual_description, f"Найдено совпадение с эталонным значением: {description}"

    @allure.step("Удаляю получателя")
    def delete_recipient(self, base_url, page_fixture):
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
            self.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

        with allure.step("Считаю количество записей в листинге(после удаления)"):
            recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

            number_of_records_after_deleting = 0
            for title in recipient_titles:
                number_of_records_after_deleting += 1
            print(number_of_records_after_deleting)

        with allure.step("Проверяю, что запись была удалена"):
            assert number_of_records_before_deleting == number_of_records_after_deleting + 1

    @allure.step("Удаляю адрес")
    def delete_adress(self, base_url, page_fixture):
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
            self.obtaining_block.adress_listing_activation_try(base_url, page_fixture)

        with allure.step("Считаю количество записей в листинге(после удаления)"):
            adress_titles = self.page.locator(self.adress_listing.INFO_TITLE).all_text_contents()

            number_of_records_after_deleting = 0
            for title in adress_titles:
                number_of_records_after_deleting += 1
            print(number_of_records_after_deleting)

        with allure.step("Проверяю, что запись была удалена"):
            assert number_of_records_before_deleting == number_of_records_after_deleting + 1

    @allure.step("Отменяю удаление")
    def cancel_recipient_deletion(self, base_url, page_fixture):
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
        self.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.recipient_listing.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.recipient_listing.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"

    @allure.step("Закрываю окно удаления")
    def close_recipient_deletion_modal(self, base_url, page_fixture):
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

        self.recipient_listing.open_recipient_listing_try(base_url, page_fixture)

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

    ADD_FIRST_ADRESS_BUTTON = "#shipping .CheckoutSection__Body .SectionInfo__ButtonAdd"
    CHANGE_BUTTON = "#shipping .CheckoutSection__Body .SectionInfo__Button"
    ADRESS_INFO = "#shipping .CheckoutSection__Body span.SectionInfo__Title"
    TYPE_PICKUP_POINT = "#shipping .CheckoutSection__Body span.SectionInfo__Info"
    PICKUP_POINT_ADRESS = "#shipping .CheckoutSection__Body .SectionInfo__Title"
    PICKUP_POINT_BUTTON = "button.CheckoutShippingControl__Button span:has-text('Пункт выдачи')"
    COURIER_BUTTON = "button.CheckoutShippingControl__Button span:has-text('Курьером')"

    def __init__(self, page: Page):
        self.page = page
        self.adress_listing = AdressListing(page)

    @allure.step("Открываю листинг адресов")
    def adress_listing_activation(self):
        self.page.locator(self.CHANGE_BUTTON).wait_for(timeout=3000)
        self.page.locator(self.CHANGE_BUTTON).click()



    @allure.step("Открываю листинг получателей")
    def adress_listing_activation_try(self, base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        adress_listing_opened = False

        # Попытка открыть список получателей
        try:
            checkout_page.obtaining_block.adress_listing_activation()
            adress_listing_opened = True
        except Exception:
            pass  # Игнорируем ошибку, продолжаем

        # Попытка нажать кнопку "Добавить первого получателя"
        if not adress_listing_opened:  # Только если предыдущее действие не сработало
            try:
                checkout_page.obtaining_block.click_first_adress_button()
                recipient_listing_opened = True
            except Exception:
                pass  # Игнорируем ошибку, продолжаем

        # Если хотя бы одно из действий сработало, продолжаем
        if adress_listing_opened:
            pass

    # Локатор адреса ПВЗ в блоке Получение
    def pickup_point_adress(self):
        return self.page.locator(self.PICKUP_POINT_ADRESS)

    @allure.step("Открываю листинг адресов ПВЗ")
    def pickup_point_adress_listing_activation(self):
        self.page.locator(self.PICKUP_POINT_BUTTON).click()

    @allure.step("Открываю листинг адресов доставки курьером")
    def courier_adress_listing_activation(self):
        self.page.locator(self.COURIER_BUTTON).click()

    @allure.step("Запоминаю адрес в блоке Получение")
    def check_out_adress(self):
        return self.page.locator(self.ADRESS_INFO).inner_text()

    @allure.step("Нажимаю на Выберите способ и адрес получения")
    def click_first_adress_button(self):
        self.page.locator(self.ADD_FIRST_ADRESS_BUTTON).wait_for(timeout=3000)
        return self.page.locator(self.ADD_FIRST_ADRESS_BUTTON).click()

    @allure.step("Создаю новый адрес")
    def create_address(self, base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        adress_listing_opened = False

        # Попытка открыть список получателей
        try:
            checkout_page.obtaining_block.adress_listing_activation()
            adress_listing_opened = True
        except Exception:
            pass  # Игнорируем ошибку, продолжаем

        # Попытка нажать кнопку "Добавить первого получателя"
        if not adress_listing_opened:  # Только если предыдущее действие не сработало
            try:
                checkout_page.obtaining_block.click_first_adress_button()
                adress_listing_opened = True
            except Exception:
                pass  # Игнорируем ошибку, продолжаем

        # Если хотя бы одно из действий сработало, продолжаем
        if adress_listing_opened:
            checkout_page.adress_listing.click_add_adress_button()
            # Выбор ПВЗ с кастомным событием (ПВЗ СДЕК)
            pickup_point_id = "84ac7315-76f0-4506-8f69-6f28f6d249c6"
            target_lat = 59.941833
            target_lon = 30.189611
            checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)
            checkout_page.map.click_pick_up_here_button()

    @allure.step("Создаю новый инфор")
    def create_address_infor(self, base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        adress_listing_opened = False

        # Попытка открыть список получателей
        try:
            checkout_page.obtaining_block.adress_listing_activation()
            adress_listing_opened = True
        except Exception:
            pass  # Игнорируем ошибку, продолжаем

        # Попытка нажать кнопку "Добавить первого получателя"
        if not adress_listing_opened:  # Только если предыдущее действие не сработало
            try:
                checkout_page.obtaining_block.click_first_adress_button()
                adress_listing_opened = True
            except Exception:
                pass  # Игнорируем ошибку, продолжаем

        # Если хотя бы одно из действий сработало, продолжаем
        if adress_listing_opened:
            checkout_page.adress_listing.click_add_adress_button()
            # Выбор ПВЗ с кастомным событием (ПВЗ СДЕК)
            pickup_point_id = "91205755-f642-4e51-8639-bf7e0a007ccf"
            target_lat = 59.807947
            target_lon = 30.468859
            checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)
            checkout_page.map.click_pick_up_here_button()

    @allure.step("Создаю новый адрес гарвин ПВЗ")
    def create_address_pvz_garwin(self, base_url, page_fixture):
        checkout_page = CheckoutPage(page_fixture)
        checkout_page.open(base_url)
        adress_listing_opened = False

        # Попытка открыть список получателей
        try:
            checkout_page.obtaining_block.adress_listing_activation()
            adress_listing_opened = True
        except Exception:
            pass  # Игнорируем ошибку, продолжаем

        # Попытка нажать кнопку "Добавить первого получателя"
        if not adress_listing_opened:  # Только если предыдущее действие не сработало
            try:
                checkout_page.obtaining_block.click_first_adress_button()
                adress_listing_opened = True
            except Exception:
                pass  # Игнорируем ошибку, продолжаем

        # Если хотя бы одно из действий сработало, продолжаем
        if adress_listing_opened:
            checkout_page.adress_listing.click_add_adress_button()
            # Выбор ПВЗ с кастомным событием (ПВЗ ГАРВИН)
            pickup_point_id = "7fff251a-3dee-4fdf-818b-87d6c180aa73"
            target_lat = 55.7040707
            target_lon = 37.6902614
            checkout_page.adress_listing.select_pickup_point(pickup_point_id, target_lat, target_lon)
            checkout_page.map.click_pick_up_here_button()



    # @allure.step("Удвляб адрес")
    # def address_deletion(self):
    #     self.adress_listing.open_action_menu()
    #     self.delete_conformation_modal.delete_adress()


"""Листинг адресов"""


class AdressListing:

    ADRESS_LISTING_MODAL = ".AddressSelection .flexColumn.KitModal__Inner"
    ADD_ADRESS_BUTTON = "button.AddressSelection__ButtonAdd"
    ACTION_MENU = ".AddressSelection__Item .AddressSelection__ButtonEdit"
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

    def __init__(self, page: Page):
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

    @allure.step("Переключаю на неактивный адрес")
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

    # @allure.step("Открываю экшн меню")
    # def open_action_menu(self):
    #     with allure.step("Нахожу блок с активной радиокнопкой"):
    #         parent_block = self.page.locator(self.CHECKED_ADRESS_BLOCK)
    #
    #         if parent_block.count() > 0:  # Проверяем, есть ли активный блок
    #             with allure.step("Нажимаю на экшн меню в активном блоке"):
    #                 self.page.locator(self.ACTION_MENU).nth(0).click()
    #         else:
    #             with allure.step("Блок с активной радиокнопкой не найден, выбираю первый невыбранный"):
    #                 parent_block = self.page.locator(self.UNSELECTED_RADIO_BUTTON).first.locator("xpath=ancestor::li")
    #                 with allure.step("Нажимаю на экшн меню в новом выбранном блоке"):
    #                     parent_block.locator(self.ACTION_MENU).click()
    #
    #     # self.page.locator(self.ACTION_MENU).nth(0).click()
    #     with allure.step("Проверяю, что экшн меню открыто"):
    #         try:
    #             expect(self.page.locator(self.ACTION_MENU_MODAL)).to_be_enabled()
    #         except AssertionError:
    #             with allure.step("Экшн меню не открылось, пробую еще раз"):
    #                 parent_block.locator(self.ACTION_MENU).click()
    #                 expect(self.page.locator(self.ACTION_MENU_MODAL)).to_be_enabled()
    #     with allure.step("Проверяю, что в меню отображаются кнопки Редактировать и Удалить"):
    #         expect(self.page.locator(self.EDIT_BUTTON)).to_be_visible()
    #         expect(self.page.locator(self.DELETE_BUTTON)).to_be_visible()

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

    def __init__(self, page: Page):
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

    DELIVERY_PRICE = "span .SelectButton__Button__Description"
    DELIVERY_DATE = "#delivery span .SelectButton__Button__Title"
    PRODUCT_PRICE = "p.CheckoutDeliveryProduct__Price"
    DELIVERY_SUMM_PRICE = "p.CheckoutDeliveryInfo__Total"


    def __init__(self, page: Page):
        self.page = page

    @allure.step("Запоминаю первоначальную стоимость товара")
    def base_price(self):
        text_base_price = self.page.locator(self.PRODUCT_PRICE).inner_text()
        base_price_number = float(text_base_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽/шт.', '')
                                  .replace('\xa0', ''))
        return base_price_number

    @allure.step("Запоминаю первоначальную стоимость товара + доставка")
    def delivery_summ_price(self):
        text_delivery_summ_price = self.page.locator(self.DELIVERY_SUMM_PRICE).inner_text()
        delivery_summ_price_number = float(text_delivery_summ_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.')
                                           .replace(' ₽/шт.', '').replace('\xa0', '').replace('Сумма:', '').replace('₽', ''))
        return delivery_summ_price_number

    @allure.step("Считываю стоимость доставки")
    def delivery_price(self):
        if self.page.locator(self.DELIVERY_PRICE).is_visible(timeout=3000):
            text_delivery_price = self.page.locator(self.DELIVERY_PRICE).inner_text()
            if text_delivery_price == "бесплатно":
                delivery_price_number = text_delivery_price
                return delivery_price_number
            else:
                delivery_price_number = float(
                    text_delivery_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽', '')
                    .replace('\xa0', ''))
                return delivery_price_number
        elif self.page.locator(self.DELIVERY_DATE).is_visible(timeout=3000):
            text_delivery_date = self.page.locator(self.DELIVERY_DATE).inner_text()
            if text_delivery_date == "Уточнить у менеджера":
                delivery_price_number = text_delivery_date
                return delivery_price_number
            else:
                raise ValueError("Элемент не найден")


"""Блок Калькуляции"""


class CalculationBlock:
    PRODUCTS_PRICE = ".flexRow-JCSB.OrderTotal__Row:has-text('Товары') .Price__Value"
    DISCOUNT_PRICE = ".flexRow-JCSB.OrderTotal__Row:has-text('Ваша скидка:') .Price__Value"
    ORDER_BUTTON = ".OrderTotal__Button"
    TOTAL_PRICE_VALUE = ".OrderTotal__Summary .Price__Value"
    DELIVERY_PRICE = ".flexRow-JCSB-AIC.OrderTotal__Row .Price__Value"
    DELIVERY_PRICE_STR = ".flexRow-JCSB-AIC.OrderTotal__Row .OrderTotal__Row__Value.--has-highlight"
    PRIVACY_POLICY_BUTTON = "a[href='/web-customer-terms']"
    OFFER_CONTRACT_BUTTON = "a[href='/oferta']"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Читаю сумму в блоке Калькуляция")
    def total_price_value(self):
        with allure.step("Извлекаю текст итоговой суммы в блоке Калькуляция"):
            text_total_price = self.page.locator(self.TOTAL_PRICE_VALUE).inner_text()
            total_price_number = float(text_total_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽', '')
                                       .replace('\xa0', ''))
            return total_price_number

    @allure.step("Нажимаю на кнопку 'Оформить заказ'")
    def click_order_button(self):
        self.page.locator(self.ORDER_BUTTON).click()

    @allure.step("Проверяю статус кнопки Оформить заказ")
    def order_button_status(self):
        return self.page.locator(self.ORDER_BUTTON)

    @allure.step("Запоминаю стоимость доставки")
    def delivery_price(self):
        # Проверяем, есть ли в строке доставки элемент с числовым значением
        if self.page.locator(self.DELIVERY_PRICE).is_visible():
            # Если элемент есть, то стоимость доставки в цифрах
            text_delivery_price = self.page.locator(self.DELIVERY_PRICE).inner_text()
            delivery_price_number = float(
                text_delivery_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽', '')
                .replace('\xa0', ''))
        else:
            # Если элемента нет, то стоимость доставки "бесплатно" или "не определено"
            text_delivery_price = self.page.locator(self.DELIVERY_PRICE_STR).inner_text().strip()
            delivery_price_number = text_delivery_price

        return delivery_price_number

    @allure.step("Запоминаю сумму скидок")
    def discount_price(self):
        text_discount_price = self.page.locator(self.DISCOUNT_PRICE).inner_text()
        discount_price_number = float(text_discount_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.')
                                      .replace(' ₽', '').replace('\xa0', ''))
        return discount_price_number

    @allure.step("Запоминаю cтоимость оформляемых заказов")
    def products_price(self):
        text_products_price = self.page.locator(self.PRODUCTS_PRICE).inner_text()
        products_price_number = float(text_products_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.')
                                      .replace(' ₽', '').replace('\xa0', ''))
        return products_price_number

    @allure.step("Нажимаю на сссылку 'Политика конфиденциальности'")
    def click_privacy_policy(self):
        self.page.locator(self.PRIVACY_POLICY_BUTTON).click()

    @allure.step("Нажимаю на сссылку 'Договор-оферта'")
    def click_offer_contract(self):
        self.page.locator(self.OFFER_CONTRACT_BUTTON).click()


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

    def __init__(self, page: Page):
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


"""Блок Оплата"""


class PaymentBlock:

    PAYMENT_ON_RECEIPT_BUTTON = "#payment button:has-text('Оплата при получении')"
    PAYMENT_BY_INVOICE = "#payment button:has-text('Оплата по счету')"
    ONLINE_PAYMENT_BUTTON = "#payment button:has-text('Онлайн-оплата')"
    CONTACT_A_MANAGER_BUTTON = "#payment button:has-text('Уточнить у менеджера')"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Получаю статус кнопки Оплата при получении")
    def payment_on_receip_button_status(self):
        return self.page.locator(self.PAYMENT_ON_RECEIPT_BUTTON)

    @allure.step("Нажимаю на кнопку Оплата при получении")
    def click_payment_on_receip_button(self):
        self.page.locator(self.PAYMENT_ON_RECEIPT_BUTTON).click()

    @allure.step("Получаю статус кнопки Оплата по счету")
    def payment_by_invoice_button_status(self):
        return self.page.locator(self.PAYMENT_BY_INVOICE)

    @allure.step("Нажимаю на кнопку Оплата по счету")
    def click_payment_by_invoice_button(self):
        self.page.locator(self.PAYMENT_BY_INVOICE).click()

    @allure.step("Получаю статус кнопки Онлайн-оплата")
    def online_payment_button_status(self):
        return self.page.locator(self.ONLINE_PAYMENT_BUTTON)

    @allure.step("Нажимаю на кнопку Онлайн-оплата")
    def click_online_payment_button(self):
        self.page.locator(self.ONLINE_PAYMENT_BUTTON).click()

    @allure.step("Получаю статус кнопки Уточнить у менеджера")
    def contact_a_manager_button_status(self):
        return self.page.locator(self.CONTACT_A_MANAGER_BUTTON)

    @allure.step("Нажимаю на кнопку Уточнить у менеджера")
    def click_contact_a_manager_button(self):
        self.page.locator(self.CONTACT_A_MANAGER_BUTTON).click()


"""Блок Комментарий"""


class CommentaryBlock:

    COMMENTARY_TOGGLE_BUTTON = "button.CheckoutSection__Toggle"
    COMMENTARY_TEXTAREA = "textarea.kit-textarea"

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Нажимаю на кнопку Комментарий к заказу")
    def click_commentary_togle_button(self):
        self.page.locator(self.COMMENTARY_TOGGLE_BUTTON).click()

    @allure.step("Ввожу значение в поле Комментарий")
    def fill_commentary_textarea(self, text):
        self.page.locator(self.COMMENTARY_TEXTAREA).fill(text)



#
# page-url: https://garwin.ru/checkout
# pointer-click: rn:710765266:x:32504:y:23772:t:85958:p:****AAA3AAAA1A1AA1A2AA1AA2AA1A1:X:1167:Y:246
# browser-info: u:1734619901805257952:v:1551:vf:14pwap7gbnncs44tf8xglmzmdcdb:rqnl:1:st:1736765012
# t: gdpr(14)ti(1)

# TODO включить в методы создания пользователя фикстуру удаления пользователя, удалить фикстуру из тестов
# TODO включить в методы создания адреса фикстуру удаления пользователя, удалить фикстуру из тестов
