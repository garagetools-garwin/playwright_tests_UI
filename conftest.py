import pytest
import allure
import os

# Фильтрация секций отчета
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Добавляем информацию о результате теста в запрос
    setattr(item, "rep_" + report.when, report)

    # Удаляем ненужные секции из отчета
    exclude_fixtures = {
        "pytestconfig", "_verify_url", "event_loop_policy", "base_url",
        "delete_output_dir", "playwright", "browser_type_launch_args",
        "browser_type", "browser", "launch_browser", "browser_context_args",
        "device", "context", "page", "page_fixture"
    }

    # Фильтруем автоматически создаваемые шаги
    report.sections = [
        section for section in report.sections if not any(fixture in section[0] for fixture in exclude_fixtures)
    ]
@pytest.fixture(scope="function")
def page_fixture(page, request):
    page.set_viewport_size({"width": 1920, "height": 1080})

    # Начало записи трассировки
    trace_path = os.path.join(os.getcwd(), f'traces/{request.node.name}.zip')
    page.context.tracing.start(screenshots=True, snapshots=True)

    # # Получаем имя браузера
    # browser_name = page.context.browser.browser_type.name
    #
    # # Получаем версию браузера
    # browser_version = page.context.browser.version
    #
    # # Добавляем сессию в отчет
    # allure.attach(
    #     name="browser_context",
    #     body=f"Browser: {browser_name}\nVersion: {browser_version}",
    #     attachment_type=allure.attachment_type.TEXT
    # )
    #
    # yield page

    # # Добавляем сессию в отчет
    # allure.attach(
    #     name="browser_context",
    #     body=page.context.browser.browser_type.name,
    #     attachment_type=allure.attachment_type.TEXT
    # )
    #
    yield page

    # Проверяем, был ли тест успешным
    if request.node.rep_call.failed:
        # Сохраняем трассировку
        page.context.tracing.stop(path=trace_path)

        # Добавляем трассировку как артефакт в Allure-отчет
        allure.attach.file(trace_path, name="trace", attachment_type='application/zip', extension='.zip')

        allure.attach(
            name="failure_screenshot",
            body=page.screenshot(full_page=True),
            attachment_type=allure.attachment_type.PNG
    ***REMOVED***
        allure.attach(
            name="page_source",
            body=page.content(),
            attachment_type=allure.attachment_type.HTML
    ***REMOVED***
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
***REMOVED***



@pytest.fixture(scope="session")
def base_url(request):
    url = request.config.getoption('--url')
    return url




# def pytest_addoption(parser):
#     parser.addoption(
#         "--url",
#         default="https://garwin.ru", #времено, возможно тут должен быть другой url
#         help="This is request url"
# ***REMOVED***
#
#     parser.addoption(
#         "--env",
#         default="prod",
#         choices=["prod", "stage"],  # времено, возможно тут должен быть другой url
#         help="" # написать подсказку
# ***REMOVED***

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
# ***REMOVED***
#     parser.addoption(
#         "--headless", action="store_true",
#         help="Run tests in headless mode"
# ***REMOVED***
#     parser.addoption(
#         "--url", default="https://garwin.ru"
#         #         "--url", default="https://stage.garagetools.ru/"
# ***REMOVED***
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
#         ***REMOVED***
#         yield browser
#         browser.close()
#
# @pytest.fixture(scope="session")
# def context(browser, base_url, browser_context_args):
#     context = browser.new_context(
#         viewport=browser_context_args['viewport']
# ***REMOVED***
#     yield context
#     context.close()
#
# @pytest.fixture(scope="function")
# def page(context):
#     page = context.new_page()
#     yield page
#     page.close()