import random
import allure
from faker import Faker
from playwright.sync_api import expect
import requests

fake = Faker('ru_RU')


class CheckoutPage:

    PATH = "/checkout"

    """Промокод"""
    PROMO_CODE_FIELD_INFO = ".Field__Info .Field__Text"
    CLEAR_PROMO_CODE_FIELD_BUTTON = ".flexRow-C.FieldControls__Button.active"
    PROMO_CODE_FIELD = ".kit-input.Field__Input.disable-label"
    PROMO_CODE_FIELD_CHECK = ".Field.PromoWidget__Field.is-small.has-controls"
    PROMO_CODE_HINT_ICON = "div.Tooltip__Icon"
    PROMO_CODE_HINT_POPUP = ".Tooltip__Inner.v-enter-to .Tooltip__Content"
    CANCEL_PROMO_CODE_BUTTON = ".flexRow-AIC.PromoWidget__CancelButton"
    PROMO_CODE_TOGGLE_BUTTON = ".PromoWidget__ToggleButton"
    PROMO_CODE_APPLY_BUTTON = ".PromoWidget__SubmitButton.Button.size--normal.color--secondary"
    PRODUCT_PRICE = "p.CheckoutDeliveryProduct__Price"

    """Блок Покупатель и получатель"""
    RECIPIENT_CHANGE_BUTTON = "#contacts .SectionInfo__Button"
    CUSTOMER_NAME = "#contacts .CheckoutSection__Custom span.SectionInfo__Title"
    RECIPIENT_INFO = "#contacts .CheckoutSection__Body span.SectionInfo__Title"

    """Листинг получателей"""
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

    """Модалка подтверждения удаления"""
    CONFIRM_DELETE_BUTTON = "div.RecipientSelectionConfirm__Buttons span:has-text('Удалить')"
    CANCEL_DELETE_BUTTON = "div.RecipientSelectionConfirm__Buttons span:has-text('Отмена')"

    # """Модалка Новый получатель"""
    # NEW_RECIPIENT_MODAL = ".RecipientSelectionAdd .flexColumn.KitModal__Inner"
    # NAME_FIELD = "div.RecipientSelectionAdd__Input input[type='text']"
    # TEL_FIELD = "div.RecipientSelectionAdd__Input input[type='tel']"
    # EMAIL_FIELD = "div.RecipientSelectionAdd__Input input[type='email']"
    # SAVE_NEW_RECIPIENT_BUTTON = "button.RecipientSelectionAdd__Button"
    # CLOSE_BUTTON = ".RecipientSelectionAdd .KitModal__Closer"

    # """Модалка новый получатель/изменить получателя"""
    # # NEW_RECIPIENT_MODAL = ".RecipientSelectionAdd .flexColumn.KitModal__Inner"
    # NAME_FIELD = "input[type='text']"
    # TEL_FIELD = "input[type='tel']"
    # EMAIL_FIELD = "input[type='email']"
    # SAVE_NEW_RECIPIENT_BUTTON = "button.RecipientSelectionAdd__Button"
    # CLOSE_BUTTON = ".RecipientSelectionAdd .KitModal__Closer"



    """Листинг адресов"""
    ADRESS_LISTING_MODAL = ".AddressSelection .flexColumn.KitModal__Inner"

    """Чек-аут"""
    ORDER_BUTTON = ".OrderTotal__Button.Button.size--medium.color--primary"

    def __init__(self, page):
        self.page = page
        self.add_modal = AddRecipientModal(page)
        self.edit_modal = EditRecipientModal(page)
        self.recipient_listing = RecipientListing(page)
        self.obtaining_block = ObtainingBlock(page)
        self.adress_listing = AdressListing(page)

    def open(self, url):
        with allure.step(f"Открываю {url + self.PATH}"):
            self.page.goto(url + self.PATH)

    """ Блок 'Промокод' """

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


    """Блок Калькуляции"""


    # @allure.step("Запоминаю стоимость скидки")
    # def discounted_price(self):
    #     text_discounted_price = self.page.locator(self.PRODUCT_PRICE_DISCOUNTED).inner_text()
    #     discounted_price_number = float(text_discounted_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.'))
    #     return discounted_price_number


    @allure.step("Запоминаю первоначальную стоимость товара")
    def base_price(self):
        text_base_price = self.page.locator(self.PRODUCT_PRICE).inner_text()
        base_price_number = float(text_base_price.replace('\n\n\xa0\n\n₽', '').replace(',', '.').replace(' ₽/шт.', ''))
        return base_price_number

    """Блок Покупатель и получатель"""
    """Модалка нового получателя"""

    @allure.step("Добавляю получателя")
    def add_recipient(self):
        self.page.locator(self.ADD_RECIPIENT_BUTTON).click()
        with allure.step("Проверяю, что модальное окно нового пользователя открыто"):
            expect(self.page.locator(self.add_modal.RECIPIENT_MODAL)).to_be_visible()

    @allure.step("Проверяю текст в блоке получателя")
    def verify_recipient_info(self, expected_info):
        actual_info = self.page.locator(self.RECIPIENT_INFO).inner_text()
        assert actual_info.lower() == expected_info.lower(), f"Expected '{expected_info}', but got '{actual_info}'"

    @allure.step("Проверяю, что новый получатель появился в листинге, его информация соответствует заданной, он активен")
    def verify_selected_recipient_info(self, expected_title, expected_description):
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        with allure.step("Сравниваю с ожидаемыми значениями"):
            assert actual_title.lower() == expected_title.lower(), f"Ожидалось: {expected_title}, Получено: {actual_title}"
            assert actual_description == expected_description, f"Ожидалось: {expected_description}, Получено: {actual_description}"

    """Листинг получателей"""

    @allure.step("Открываю листинг получателей")
    def open_recipient_listing(self):
        self.page.locator(self.RECIPIENT_CHANGE_BUTTON).click()
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
            actual_info_check_out = self.page.locator(self.RECIPIENT_INFO).inner_text()

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
    def delete_recipient(self):
        self.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        self.delete_confirm()
        self.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        for title in recipient_titles:
            assert title != actual_title, f"Найдено совпадение с эталонным значением: {title}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.INFO_DESCRIPTION).all_text_contents()

        for description in recipient_descriptions:
            assert description != actual_description, f"Найдено совпадение с эталонным значением: {description}"


    @allure.step("Отменяю удаление")
    def cancel_recipient_deletion(self):
        self.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        self.cancel_deletion()
        self.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"


    @allure.step("Закрываю окно удаления")
    def close_recipient_deletion_modal(self):
        self.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        self.page.mouse.click(0, 0)
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.CONFIRM_DELETE_BUTTON)).not_to_be_visible()

        self.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"


class AddRecipientModal:

    """Модалка Новый получатель"""
    RECIPIENT_MODAL = ".RecipientSelectionAdd .flexColumn.KitModal__Inner"
    NAME_FIELD = "div.RecipientSelectionAdd__Input input[type='text']"
    TEL_FIELD = "div.RecipientSelectionAdd__Input input[type='tel']"
    EMAIL_FIELD = "div.RecipientSelectionAdd__Input input[type='email']"
    SAVE_RECIPIENT_BUTTON = "button.RecipientSelectionAdd__Button"
    CLOSE_BUTTON = ".RecipientSelectionAdd .KitModal__Closer"

    def __init__(self, page):
        self.page = page
        self.recipient_listing = RecipientListing(page)

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


class EditRecipientModal:

    """Модалка Новый получатель"""
    RECIPIENT_MODAL = ".RecipientSelectionEdit .flexColumn.KitModal__Inner"
    NAME_FIELD = "div.RecipientSelectionEdit__Input input[type='text']"
    TEL_FIELD = "div.RecipientSelectionEdit__Input input[type='tel']"
    EMAIL_FIELD = "div.RecipientSelectionEdit__Input input[type='email']"
    SAVE_RECIPIENT_BUTTON = "button.RecipientSelectionEdit__Button"
    CLOSE_BUTTON = ".RecipientSelectionEdit .KitModal__Closer"

    def __init__(self, page):
        self.page = page
        self.recipient_listing = RecipientListing(page)


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


class ObtainingBlock:

    CHANGE_BUTTON = "#shipping .SectionInfo__Button"


    def __init__(self, page):
        self.page = page

    @allure.step("Открываю листинг адресов")
    def adress_listing_activation(self):
        self.page.locator(self.CHANGE_BUTTON).click()


class AdressListing:

    ADRESS_LISTING_MODAL = ".AddressSelection .flexColumn.KitModal__Inner"
    ADD_ADRESS_BUTTON = "button.AddressSelection__ButtonAdd"
    MAP_MODAL = "h2:has-text('Способ доставки')"
    ACTION_MENU = ".AddressSelection__ButtonEdit"
    ACTION_MENU_MODAL = ".AddressSelection__Item__Tooltip.--open-tooltip"
    EDIT_BUTTON = ".AddressSelection__Item__Tooltip.--open-tooltip span:has-text('Редактировать')"
    DELETE_BUTTON = ".AddressSelection__Item__Tooltip.--open-tooltip span:has-text('Удалить')"
    # CHANGE_RECIPIENT_MODAL = "p:has-text('Изменить получателя')"
    PICKUP_POINT_MARKER = "#ea46425d-ece1-4098-8596-ea200f01a7c9"
    SELECTED_RADIO_BUTTON = "input[type='radio']:checked"
    UNSELECTED_RADIO_BUTTON = ".Radio__Inner >> input[type='radio']:not(:checked)"
    RECIPIENT_BLOCK = "li.AddressSelection__Item"
    INFO_TITLE = ".AddressSelection__InfoTitle"
    INFO_DESCRIPTION = ".AddressSelection__InfoDescription"
    CHECKED_ADRESS_BLOCK = "li.AddressSelection__Item:has(input[type='radio']:checked)"
    ADRESS_SELECTION_BUTTON = "button.AddressSelection__ButtonChange"
    DELETE_CONFIRMATION_MODAL = "p:has-text('Вы уверены, что хотите удалить адрес доставки?')"
    #TODO: нужны два локатора при нажатии на редактировать, убедится, что пункт выдачи кнопка выделена, курьер выделен при выделения курьера и полявились поля
    # CHANGE_ADRESS_MODAL = "p:has-text('Изменить получателя')"

    def __init__(self, page):
        self.page = page

    @allure.step("Открываю листинг адресов")
    def adress_listing_modal(self):
        return self.page.locator(self.ADRESS_LISTING_MODAL)

    @allure.step("Открываю Карту")
    def map_modal(self):
        return self.page.locator(self.MAP_MODAL)

    @allure.step("Выбираю ПВЗ по координатам")
    def select_pickup_point(self, latitude: str, longitude: str):
        self.map_modal().wait_for()
        self.page.evaluate(
            """
            ([latitude, longitude]) => {
                console.log('Map instance:', window.mapInstance);
                window.ymaps && window.ymaps.ready(() => {
                    console.log('Map is ready');
                    const map = window.mapInstance;
                    console.log('Map object:', map);
                    map.events.fire('click', {
                        type: 'click',
                        target: map,
                        coords: [parseFloat(latitude), parseFloat(longitude)],
                    });
                });
            }
            """,
            [latitude, longitude]
        )
    @allure.step("Выбираю ПВЗ по ID")
    def select_pickup_point_by_id(self, point_id: str):
        self.map_modal().wait_for()
        self.page.evaluate(
            """
            (pointId) => {
                window.ymaps && window.ymaps.ready(() => {
                    const placemark = window.mapInstance.geoObjects.toArray().find(obj => obj.properties.get('id') === pointId);
                    if (placemark) {
                        placemark.events.fire('click', {
                            type: 'click',
                            target: placemark,
                        });
                    } else {
                        console.warn(`Метка с ID ${pointId} не найдена.`);
                    }
                });
            }
            """,
            point_id
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
            actual_info_check_out = self.page.locator(self.ADRESS_INFO).inner_text()

        with allure.step("Сравниваю информацию в блоке Получние с адресом выбранным в листинге "):
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
            expect(self.page.locator(self.CHANGE_ADRESS_MODAL)).to_be_visible()

    @allure.step("Нажимаю на Удалить")
    def click_delete_button(self):
        self.page.locator(self.DELETE_BUTTON).click()
        with allure.step("Проверяю, что окно подтверждения удаления отображается на странице"):
            expect(self.page.locator(self.DELETE_CONFIRMATION_MODAL)).to_be_visible()

# """Сделать класс для подтверждения удаления"""

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
    def delete_recipient(self):
        self.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        self.delete_confirm()
        self.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        for title in recipient_titles:
            assert title != actual_title, f"Найдено совпадение с эталонным значением: {title}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.INFO_DESCRIPTION).all_text_contents()

        for description in recipient_descriptions:
            assert description != actual_description, f"Найдено совпадение с эталонным значением: {description}"

    @allure.step("Отменяю удаление")
    def cancel_recipient_deletion(self):
        self.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        self.cancel_deletion()
        self.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"

    @allure.step("Закрываю окно удаления")
    def close_recipient_deletion_modal(self):
        self.click_delete_button()
        with allure.step("Нахожу блок с активной радиокнопкой"):
            # Ищем `li` с id="delivery-point", внутри которого активна радиокнопка
            parent_block = self.page.locator(self.CHECKED_RECIPIENT_BLOCK)
            assert parent_block.is_visible(), "Блок с активной радиокнопкой не найден."

        with allure.step("Ищу информацию в выбранном блоке"):
            # Извлекаем текст заголовка и описания
            actual_title = parent_block.locator(self.INFO_TITLE).inner_text()
            actual_description = parent_block.locator(self.INFO_DESCRIPTION).inner_text()

        self.page.mouse.click(0, 0)
        with allure.step("Проверяю, что окно закрыто"):
            expect(self.page.locator(self.CONFIRM_DELETE_BUTTON)).not_to_be_visible()

        self.open_recipient_listing()

        # по циклу проверяю каждый заголовок(фио) в листинге, сравниваю с удаленным получателем
        recipient_titles = self.page.locator(self.INFO_TITLE).all_text_contents()

        assert any(title == actual_title for title in recipient_titles), \
            f"ФИО {actual_title} не найдено в списке: {recipient_titles}"

        # по циклу проверяю каждое описание (мэил, телефон) в листинге, сравниваю с удаленным получателем
        recipient_descriptions = self.page.locator(self.INFO_DESCRIPTION).all_text_contents()

        assert any(description == actual_description for description in recipient_descriptions), \
            f"Телефон и мэил {actual_description} не найдены в списке: {recipient_descriptions}"

#
# page-url: https://garwin.ru/checkout
# pointer-click: rn:710765266:x:32504:y:23772:t:85958:p:****AAA3AAAA1A1AA1A2AA1AA2AA1A1:X:1167:Y:246
# browser-info: u:1734619901805257952:v:1551:vf:14pwap7gbnncs44tf8xglmzmdcdb:rqnl:1:st:1736765012
# t: gdpr(14)ti(1)

