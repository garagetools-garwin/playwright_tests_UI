import requests
import pytest

class ProductsApiClient:

# Работает для всех запросах в рамках сессии
    def __init__(self,
                 base_url="https://garwin.ru",
                 # auth_token="special-key"
                 ):
        self.session = requests.Session()
        self.session.headers = {"X-Store-Id": "garwin",
                                 # "Authorization": f"{auth_token}"
                                 }
        self.base_url = base_url
        # self.session.verify = False   # отмена проверки SSL-сертификата

    """
    Этот метод передает список slug и url. slug из основных категорий в каталоге (главная страница)
    """

    def get_home_categories(self):
        response = self.session.get(url=f"{self.base_url}/bff/v1/pages/home")
        assert response.ok, \
            f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"

        # Создаем пустой список, в который будем добавлять кортежи (slug, url)
        categories = []

        # Получаем список категорий из JSON-ответа
        json_response = response.json()
        categories_json = json_response.get('categories', [])

        # Проходим по каждой категории в списке категорий
        for category in categories_json:
            # Получаем значение slug для текущей категории
            slug = category.get('slug')
            # Проверяем, что slug не пустой (не None)
            if slug:
                # Формируем URL для текущей категории
                url = f"{self.base_url}/catalog/{slug}"
                # Добавляем кортеж (slug, url) в список категорий
                categories.append((slug, url))
            else:
                raise ValueError("Failed to get the slug for the category")
        return categories[::-1]

    """
    Этот метод передает список slug и url. slug из основных категорий в хедере (кнопка каталог)
    """
    def get_header_categories(self):
        response = self.session.get(url=f"{self.base_url}/bff/v0/categories/root")
        assert response.ok, \
            f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"

        categories = []

        json_response = response.json()
        nested_categories = json_response.get("nested_categories")

        for category in nested_categories:
            permalink = category.get("permalink")
            if permalink:
                url = f"{self.base_url}/catalog/{permalink}"
                categories.append((permalink, url))
            else:
                raise ValueError("Failed to get the permalink for the category")
        return categories[::-1]

    """
    Этот метод передает список slug и url. slug из под-категорий в хедере (кнопка каталог)
    """

    def get_header_sub_categories(self):
        response = self.session.get(url=f"{self.base_url}/bff/v0/categories/root")
        assert response.ok, \
            f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"

        categories = []

        json_response = response.json()
        nested_categories = json_response.get("nested_categories", [])
        for sub_nested_categories in nested_categories:
            for sub_category in sub_nested_categories["nested_categories"]:
                permalink = sub_category.get("permalink")
                if permalink:
                    url = f"{self.base_url}/catalog/{permalink}"
                    categories.append((permalink, url))
                else:
                    raise ValueError("Failed to get the permalink for the category")
        return categories[::-1]

    """
    Этот метод передает список slug и url. slug из под-категорий в каталоге (главная страница)
    """

    def get_category_urls(self):
        # Получаем список всех категорий
        main_categories = self.get_main_category_links_for_sub()

        # Список для хранения всех URL-адресов подкатегорий
        all_subcategory_urls = []

        # Для каждой категории получаем URL и вызываем get_catalog_sub_categories
        for slug, url in main_categories:
            subcategories = self.get_catalog_sub_categories_for_sub(url)
            all_subcategory_urls.extend(subcategories)

        return all_subcategory_urls

    def get_main_category_links_for_sub(self):
        response = self.session.get(url=f"{self.base_url}/bff/v1/pages/home")
        assert response.ok, \
            f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"

        categories = []

        json_response = response.json()
        categories_json = json_response.get('categories', [])

        for category in categories_json:
            slug = category.get('slug')
            if slug:
                url = f"{self.base_url}/bff/v1/pages/category_catalog/{slug}/products"
                categories.append((slug, url))
            else:
                raise ValueError("Failed to get the slug for the category")
        return categories[::-1]

    def get_catalog_sub_categories_for_sub(self, url):
        response = self.session.post(url=url)
        assert response.ok, \
            f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"

        categories = []

        json_response = response.json()
        facets = json_response.get("facets", [])
        for buckets in facets:
            if buckets.get('type') == 'CATEGORY':
                for sub_category in buckets["buckets"]:
                    slug = sub_category.get("slug")
                    if slug:
                        sub_url = f"{self.base_url}/catalog/{slug}"
                        categories.append((slug, sub_url))
                    else:
                        raise ValueError("Failed to get the slug for the category")
        return categories[::-1]

    """
    Этот метод передает список permalink и url включающих полученый permalink из под-категорий в хедере (кнопка каталог)
    """

    def get_catalog_sub_categories_have_products(self):
        response = self.session.get(url=f"{self.base_url}/bff/v0/categories/root")
        assert response.ok, \
            f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"

        categories = []

        json_response = response.json()
        nested_categories = json_response.get("nested_categories", [])
        for sub_nested_categories in nested_categories:
            for sub_category in sub_nested_categories["nested_categories"]:
                permalink = sub_category.get("permalink")
                if permalink:
                    url = f"{self.base_url}/bff/v1/pages/category_catalog/{permalink}/products"
                    categories.append((permalink, url))
                else:
                    raise ValueError("Failed to get the permalink for the category")
        return categories[::-1]



    # def get_home_sub_categories(self):
    #     response = self.session.post(url=f"{self.base_url}/bff/v1/pages/category_catalog/ruchnoy-instrument/products")
    #     assert response.ok, \
    #         f"Unexpected status code for URL {response.url}. Expected: 200 or 300, Actual: {response.status_code}"
    #
    #     categories = []
    #
    #     json_response = response.json()
    #     facets = json_response.get("facets", [])
    #     for buckets in facets:
    #         if buckets.get('type') == 'CATEGORY':
    #             for sub_category in buckets["buckets"]:
    #                 slug = sub_category.get("slug")
    #                 if slug:
    #                     url = f"{self.base_url}/catalog/{slug}"
    #                     categories.append((slug, url))
    #                 else:
    #                     raise ValueError("Failed to get the slug for the category")
    #     return categories[::-1]