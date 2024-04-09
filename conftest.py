import pytest

from api_clients.api_client import ProductsApiClient


@pytest.fixture()  # если токен будет постояно обнавлятся лучше оставить function
def api_client():
    client = ProductsApiClient()
    return client


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
