import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import allure
import os
from dotenv import load_dotenv
import configparser
import pytest


# Фильтрация секций отчета
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Добавляем информацию о результате теста в запрос
    setattr(item, "rep_" + report.when, report)



@pytest.fixture(scope="function")
def page_fixture(browser, request):
    # Получаем метку, чтобы определить, нужен ли storage_state
    use_auth = request.node.get_closest_marker("auth")

    if use_auth:
        # Создаём новый контекст с сохранённым состоянием авторизации, если метка присутствует
        context = browser.new_context(storage_state="auth_state.json")
    else:
        # Стандартный контекст без авторизации
        context = browser.new_context()

    # Создаём новую страницу в контексте
    page = context.new_page()

    page.set_viewport_size({"width": 1920, "height": 1080})

    # Получение текущей даты и времени
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Формирование имени файла с трассировкой
    trace_path = os.path.join(
        os.getcwd(),
        f'traces/{request.node.name}_{current_time}.zip'
    )

    os.makedirs(os.path.dirname(trace_path), exist_ok=True)
    page.context.tracing.start(screenshots=True, snapshots=True)

    # Сетевой лог
    network_logs = []

    # Перехват запросов, можно закоментить для удобства отладки тестов
    page.on("requestfinished", lambda request: network_logs.append({
        "url": request.url,
        "method": request.method,
        "status": request.response().status,
        "headers": request.response().headers,
        "body": request.post_data if request.post_data else "No data",
        "query_params": parse_qs(urlparse(request.url).query)
    }))

    page.on("requestfailed", lambda request: (
        network_logs.append({
            "url": request.url,
            "method": request.method,
            "error": getattr(request.failure, "error_text", "Unknown error"),
            "query_params": parse_qs(urlparse(request.url).query)
        }),
        print(f"Request failed with error: {getattr(request.failure, 'error_text', 'Unknown error')}")
    ))

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