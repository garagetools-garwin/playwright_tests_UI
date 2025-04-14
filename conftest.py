import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import allure
from dotenv import load_dotenv
import configparser
import pytest
from page_objects.checkout_page import CheckoutPage
from page_objects.cart_page import CartPage
from dotenv import load_dotenv
import os
import re

load_dotenv()  # Загружаем переменные из .env

AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")


# Фильтрация секций отчета
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Добавляем информацию о результате теста в запрос
    setattr(item, "rep_" + report.when, report)
    # Добавляем метку "Test Rerun" для перезапущенных тестов
    if report.outcome == "failed" and item.get_closest_marker("rerun"):
        allure.dynamic.label("rerun", "Test Rerun")

# Хук для создания папки auth_states перед началом тестов
# def pytest_configure(config):
#     project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     auth_states_dir = os.path.join(project_root, 'auth_states')
#     os.makedirs(auth_states_dir, exist_ok=True)

@pytest.fixture(scope="function")
def page_fixture(browser, request, base_url):

    # Путь к корню проекта и папке auth_states
    project_root = os.path.dirname(os.path.abspath(__file__))  # Путь к корню проекта
    auth_states_dir = os.path.join(project_root, 'auth_states')
    os.makedirs(auth_states_dir, exist_ok=True)

    auth_state_path = os.path.join(auth_states_dir, "auth_state.json")
    auth_state_empty_path = os.path.join(auth_states_dir, "auth_state_empty.json")

    # Получаем метку, чтобы определить, нужен ли storage_state
    # "auth" используется для авторизации через основной тестовый аккаунт, подходит для большенства задач
    use_auth = request.node.get_closest_marker("auth")
    # "auth_empty" используется для специального пустого аккаунта, в котором нет ниодного адреса или получателя
    # / не создавать адреса или получателей в этом аккаунте!
    use_auth_empty = request.node.get_closest_marker("auth_empty")

    if use_auth:
        # Создаём новый контекст с сохранённым состоянием авторизации, если метка присутствует
        context = browser.new_context(storage_state=auth_state_path)
    elif use_auth_empty:
        # Создаём новый контекст с сохранённым состоянием авторизации, если метка присутствует
        context = browser.new_context(storage_state=auth_state_empty_path)
    else:
        # Стандартный контекст без авторизации
        context = browser.new_context()

    # Создаём новую страницу в контексте
    page = context.new_page()

    # Если платформа тестовая, автоматически авторизуемся через URL
    if "https://stage.garwin.ru" in base_url or "https://review-site" in base_url:
        auth_url = base_url.replace("https://", f"https://{AUTH_USERNAME}:{AUTH_PASSWORD}@")
        page.goto(auth_url)
        context.storage_state(path=auth_state_path)

    page.set_viewport_size({"width": 1920, "height": 1080})
    # Задаем куки онбордингов для того, чтобы они не всплывали в тестах
    context.add_cookies([{"name": "onboarding__search", "value": "true", "url": f"{base_url}"},
                         {"name": "onboarding__filters", "value": "true", "url": f"{base_url}"},
                         {"name": "onboarding__legalEntities", "value": "true", "url": f"{base_url}"}
                         ])

    # Получение текущей даты и времени
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Удаляем все символы, которые нельзя использовать в путях Windows
    safe_name = re.sub(r'[\\/*?:"<>|\[\]]', '_', request.node.name)

    # Формирование имени файла с трассировкой
    trace_path = os.path.join(
        os.getcwd(),
        f'traces/{safe_name}_{current_time}.zip'
    )

    os.makedirs(os.path.dirname(trace_path), exist_ok=True)
    page.context.tracing.start(screenshots=True, snapshots=True)

    # Сетевой лог
    network_logs = []

    # Перехват запросов, можно закоментить для удобства отладки тестов
    # page.on("requestfinished", lambda request: network_logs.append({
    #     "url": request.url,
    #     "method": request.method,
    #     "status": request.response().status,
    #     "headers": request.response().headers,
    #     "body": request.post_data if request.post_data else "No data",
    #     "query_params": parse_qs(urlparse(request.url).query)
    # }))
    #
    # page.on("requestfailed", lambda request: (
    #     network_logs.append({
    #         "url": request.url,
    #         "method": request.method,
    #         "error": getattr(request.failure, "error_text", "Unknown error"),
    #         "query_params": parse_qs(urlparse(request.url).query)
    #     }),
    #     print(f"Request failed with error: {getattr(request.failure, 'error_text', 'Unknown error')}")
    # ))

    yield page

    # Проверяем, был ли тест успешным
    if request.node.rep_call.failed:
        # Сохраняем трассировку
        page.context.tracing.stop(path=trace_path)

        # Формирование имени файла с логами
        log_path = os.path.join(
            os.getcwd(),
            f'logs/{request.node.name}_{current_time}_network_logs.json'
        )
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        with open(log_path, 'w') as log_file:
            json.dump(network_logs, log_file, indent=4)

        # Добавляем трассировку как артефакт в Allure-отчет
        allure.attach.file(
            trace_path,
            name="trace",
            attachment_type='application/zip',
            extension='.zip')

        allure.attach(
            name="failure_screenshot",
            body=page.screenshot(full_page=True),
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            name="page_source",
            body=page.content(),
            attachment_type=allure.attachment_type.HTML
        )
        allure.attach.file(
            log_path,
            name="network_logs",
            attachment_type=allure.attachment_type.JSON
        )
    else:
        # Если тест успешен, просто останавливаем трассировку без сохранения
        page.context.tracing.stop()

    # Закрываем контекст браузера
    page.context.close()

def pytest_addoption(parser):
    # TODO Здесь будет настройка переключения браузера
    # parser.addoption(
    #     "--browser", default="ch", choices=["ya", "ch", "ff"]
    # На случай смены headless режима
    # )
    # parser.addoption(
    #     "--headless", action="store_true"
    # )
    parser.addoption(
        "--url", default="https://garwin.ru"
        # "--url", default="https://stage.garagetools.ru/"
    )


"""Фикстура для подмены нового контекста авторизованным"""


@pytest.fixture(scope="function")
def authorized_context(browser):
    # Передаем состояние авторизации для создания контекста
    return {
        "storage_state": "auth_state.json"
    }


@pytest.fixture(scope="session")
def base_url(request):
    url = request.config.getoption('--url')
    return url


"""Фикстуры для тестов"""

# Старая, простая, но рабочая версия фикстуры
# @pytest.fixture
# def delete_address_fixture(request, page_fixture, base_url):
#     """Фикстура для удаления записи после завершения теста."""
#     checkout_page = CheckoutPage (page_fixture)
#     address_created = False  # Локальный флаг в рамках фикстуры
#
#     def mark_as_created():
#         nonlocal address_created
#         address_created = True
#
#     def teardown():
#         if address_created:
#             with allure.step("Удаляю созданный адрес"):
#                 checkout_page.open(base_url)
#                 checkout_page.obtaining_block.adress_listing_activation()
#                 checkout_page.adress_listing.open_action_menu()
#                 checkout_page.delete_conformation_modal.delete_adress()
#
#     request.addfinalizer(teardown)  # Добавляем выполнение удаления при завершении теста
#     return mark_as_created





@pytest.fixture
def delete_recipient_fixture(request, page_fixture, base_url):
    """Фикстура для удаления записи после завершения теста."""
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    recipient_created = False  # Флаг создания получателя
    recipient_deleted = False  # Флаг удаления получателя

    def mark_as_created():
        """Помечает, что получатель был создан."""
        nonlocal recipient_created
        recipient_created = True

    def teardown():
        nonlocal recipient_deleted

        if recipient_created and not recipient_deleted:
            with allure.step("Удаляю созданного получателя"):
                checkout_page.open(base_url)

                try:
                    # Проверяем сумму заказа
                    total_price = checkout_page.calculation_block.page.locator(
                        checkout_page.calculation_block.TOTAL_PRICE_VALUE
                    ).text_content(timeout=3000)
                except Exception:
                    total_price = None
                    cart_page.add_to_cart_cheap_product(base_url)
                    checkout_page.open(base_url)

                # Проверяем актуальную сумму
                price = checkout_page.calculation_block.total_price_value()
                print(price)

                if not price or price == 0:
                    cart_page.add_to_cart_cheap_product(base_url)
                    checkout_page.open(base_url)

                # Удаляем получателя
                if not recipient_deleted:
                    checkout_page.recipient_listing.open_recipient_listing_try(base_url, page_fixture)
                    checkout_page.recipient_listing.open_action_menu()
                    checkout_page.delete_conformation_modal.delete_recipient(base_url, page_fixture)
                    recipient_deleted = True  # Запоминаем, что удаление уже произошло

    request.addfinalizer(teardown)
    return mark_as_created


@pytest.fixture
def delete_address_fixture(request, page_fixture, base_url):
    """Фикстура для удаления адреса после завершения теста."""
    checkout_page = CheckoutPage(page_fixture)
    cart_page = CartPage(page_fixture)
    address_created = False  # Флаг создания адреса
    address_deleted = False  # Флаг удаления адреса

    def mark_as_created():
        """Помечает, что адрес был создан."""
        nonlocal address_created
        address_created = True

    def teardown():
        nonlocal address_deleted

        if address_created and not address_deleted:
            with allure.step("Удаляю созданный адрес"):
                checkout_page.open(base_url)

                try:
                    # Проверяем сумму заказа
                    total_price = checkout_page.calculation_block.page.locator(
                        checkout_page.calculation_block.TOTAL_PRICE_VALUE
                    ).text_content(timeout=3000)
                except Exception:
                    total_price = None
                    cart_page.add_to_cart_cheap_product(base_url)
                    checkout_page.open(base_url)

                # Проверяем актуальную сумму
                price = checkout_page.calculation_block.total_price_value()
                print(price)

                if not price or price == 0:
                    cart_page.add_to_cart_cheap_product(base_url)
                    checkout_page.open(base_url)

                # Удаляем адрес
                if not address_deleted:
                    checkout_page.obtaining_block.adress_listing_activation_try(base_url, page_fixture)
                    checkout_page.adress_listing.open_action_menu()
                    checkout_page.delete_conformation_modal.delete_adress(base_url, page_fixture)
                    address_deleted = True  # Запоминаем, что удаление уже произошло

    request.addfinalizer(teardown)
    return mark_as_created

# Версия фикстуры на удаление с возвратом артефактов
# @pytest.fixture
# def delete_address_fixture(request, page_fixture, base_url):
#     """Фикстура для удаления записи после завершения теста."""
#     checkout_page = CheckoutPage(page_fixture)
#     address_created = False  # Флаг успешного создания адреса
#
#     # Получение текущей даты и времени для артефактов
#     current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#
#     # Формирование пути для трассировки
#     trace_path = os.path.join(
#         os.getcwd(),
#         f'traces/{request.node.name}_{current_time}.zip'
#     )
#     os.makedirs(os.path.dirname(trace_path), exist_ok=True)
#
#     # Запускаем трассировку заранее, чтобы зафиксировать возможное падение
#     page_fixture.context.tracing.start(screenshots=True, snapshots=True)
#
#     def mark_as_created():
#         nonlocal address_created
#         address_created = True
#
#     def teardown():
#         """Удаление записи и сохранение артефактов при сбое."""
#         try:
#             if address_created:
#                 with allure.step("Удаляю запись"):
#                     checkout_page.open(base_url)
#                     checkout_page.obtaining_block.adress_listing_activation()
#                     checkout_page.adress_listing.open_action_menu()
#                     checkout_page.delete_conformation_modal.delete_adress()
#         finally:
#             # Останавливаем трассировку и сохраняем её в любом случае
#             page_fixture.context.tracing.stop(path=trace_path)
#
#             # Сохраняем скриншот, даже если тест упал
#             allure.attach(
#                 name="failure_screenshot",
#                 body=page_fixture.screenshot(full_page=True),
#                 attachment_type=allure.attachment_type.PNG
#             )
#
#             # Сохраняем HTML-код страницы
#             allure.attach(
#                 name="page_source",
#                 body=page_fixture.content(),
#                 attachment_type=allure.attachment_type.HTML
#             )
#
#             # Добавляем трассировку в отчёт
#             allure.attach.file(
#                 trace_path,
#                 name="trace",
#                 attachment_type="application/zip",
#                 extension=".zip"
#             )
#
#     request.addfinalizer(teardown)  # Гарантированное выполнение teardown
#     return mark_as_created
# Конец фикстуры по удалению

#
#
# # Фикстура для выполнения кода перед тестами
# @pytest.fixture(scope="session", autouse=True)
# def set_token_in_config():
#     # Загружаем переменные из файла .env
#     load_dotenv()
#
#     # Создаём объект конфигурации
#     config = configparser.ConfigParser()
#
#     # Читаем файл config.ini
#     config.read('connection_config.ini')
#
#     # Получаем значение переменной из .env
#     env_token = os.getenv('TMS_PRIVATE_TOKEN')
#     print(os.getenv("TMS_PRIVATE_TOKEN"))
#
#     if env_token is None:
#         raise ValueError("Переменная окружения 'TMS_TOKEN' не задана!")
#
#     # Замена плейсхолдера {TMS_TOKEN} на значение переменной окружения
#     config.set('testit', 'privateToken', env_token)
#
#     # Сохраняем изменения в файл config.ini
#     with open('connection_config.ini', 'w') as configfile:
#         config.write(configfile)
#
#     print("Переменная успешно подставлена в config.ini")




# def pytest_addoption(parser):
#     parser.addoption(
#         "--url",
#         default="https://garwin.ru", #времено, возможно тут должен быть другой url
#         help="This is request url"
#     )
#
#     parser.addoption(
#         "--env",
#         default="prod",
#         choices=["prod", "stage"],  # времено, возможно тут должен быть другой url
#         help="" # написать подсказку
#     )

# @pytest.fixture
# def base_url(request):
#     return request.config.getoption("--url")


"""Косячная версия через GPT (зато работает chrome)"""
# import pytest
# from playwright.sync_api import sync_playwright
#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--playwright-browser", default="chromium", choices=["chromium", "firefox", "webkit", "chrome"],
#         help="Browser to run tests"
#     )
#     parser.addoption(
#         "--headless", action="store_true",
#         help="Run tests in headless mode"
#     )
#     parser.addoption(
#         "--url", default="https://garwin.ru"
#         #         "--url", default="https://stage.garagetools.ru/"
#     )
#
# @pytest.fixture(scope="session")
# def browser_context_args(request):
#     return {
#         "viewport": {"width": 1920, "height": 1080},
#         "headless": request.config.getoption("--headless")
#     }
#
# @pytest.fixture(scope="session")
# def base_url(request):
#     return request.config.getoption('--url')
#
# @pytest.fixture(scope="session")
# def browser(request, browser_context_args):
#     browser_name = request.config.getoption("--playwright-browser")
#     with sync_playwright() as p:
#         if browser_name == "chromium":
#             browser = p.chromium.launch(headless=browser_context_args['headless'])
#         elif browser_name == "firefox":
#             browser = p.firefox.launch(headless=browser_context_args['headless'])
#         elif browser_name == "webkit":
#             browser = p.webkit.launch(headless=browser_context_args['headless'])
#         elif browser_name == "chrome":
#             browser = p.chromium.launch(
#                 channel="chrome",
#                 headless=browser_context_args['headless']
#             )
#         yield browser
#         browser.close()
#
# @pytest.fixture(scope="session")
# def context(browser, base_url, browser_context_args):
#     context = browser.new_context(
#         viewport=browser_context_args['viewport']
#     )
#     yield context
#     context.close()
#
# @pytest.fixture(scope="function")
# def page(context):
#     page = context.new_page()
#     yield page
#     page.close()