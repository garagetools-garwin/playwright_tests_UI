import pytest


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

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {

        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }


@pytest.fixture(scope="session")
def base_url(request):
    url = request.config.getoption('--url')
    return url

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