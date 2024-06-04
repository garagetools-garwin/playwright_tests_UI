import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {

        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }

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