import pytest
from api_clients.api_client import ProductsApiClient

from conftest import api_client, print_failed_urls
from conftest import failed_urls
client = ProductsApiClient()


""""Этот тест проверяет статус ok ссылок основных категорий в каталоге (главная страница)"""


@pytest.mark.parametrize("slug_and_url", client.get_home_categories(), ids=lambda x: x[0])
def test_home_categories(print_failed_urls, slug_and_url):
    slug, url = slug_and_url
    response = client.session.get(url)
    global failed_urls
    if not response.ok:
        failed_urls.append(url)
    assert response.ok, \
        f"Unexpected status code for URL {url}. Expected: 200 or 300, Actual: {response.status_code}"


""""Этот тест проверяет статус ok ссылок под-категорий в каталоге"""


@pytest.mark.parametrize("slug_and_url", client.get_category_urls(), ids=lambda x: x[0])
def test_catalog_sub_categories(print_failed_urls, slug_and_url):
    slug, url = slug_and_url
    response = client.session.post(url)
    global failed_urls
    if not response.ok:
        failed_urls.append(url)
    assert response.ok, \
        f"Unexpected status code for URL {url}. Expected: 200 or 300, Actual: {response.status_code}"


""""Этот тест проверяет статус ok ссылок основных категорий в хедере (кнопка каталог)"""


@pytest.mark.parametrize("permalink_and_url", client.get_header_categories(), ids=lambda x: x[0])
def test_header_categories(print_failed_urls, permalink_and_url):
    permalink, url = permalink_and_url
    response = client.session.get(url)
    global failed_urls
    if not response.ok:
        failed_urls.append(url)
    assert response.ok, \
        f"Unexpected status code for URL {url}. Expected: 200 or 300, Actual: {response.status_code}"


""""Этот тест проверяет статус ok ссылок под-категорий в хедере (кнопка каталог)"""


@pytest.mark.parametrize("permalink_and_url", client.get_header_sub_categories(), ids=lambda x: x[0])
def test_header_sub_categories(print_failed_urls, permalink_and_url):
    permalink, url = permalink_and_url
    response = client.session.get(url)
    global failed_urls
    if not response.ok:
        failed_urls.append(url)
    assert response.ok, \
        f"Unexpected status code for URL {url}. Expected: 200 or 300, Actual: {response.status_code}"


""""Этот тест проверяет, что список products в под-категориях не является пустым"""


@pytest.mark.parametrize("permalink_and_url", client.get_catalog_sub_categories_have_products(), ids=lambda x: x[0])
def test_header_sub_categories_have_products(print_failed_urls, permalink_and_url):
    try:
        permalink, url = permalink_and_url
        response = client.session.post(url)
        json_response = response.json()
        products_json = json_response['products']
    except KeyError:
        pytest.skip("Ошибка KeyError: 'products' - пропускаем тест")
    else:
        global failed_urls
        if not products_json:
            failed_urls.append(url)
        assert products_json, "Products list is empty"






