import pytest

from api_clients.api_client import ProductsApiClient


@pytest.fixture()  # если токен будет постояно обнавлятся лучше оставить function
def api_client():
    client = ProductsApiClient()
    return client


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

@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")

failed_urls = []
@pytest.fixture(scope="session", autouse=True)
def print_failed_urls():
    yield
    if failed_urls:
        print("\nFailed URLs:")
        for url in failed_urls:
            print(url)

    # Очистить список после вывода
    failed_urls.clear()
