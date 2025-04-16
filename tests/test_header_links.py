import re
import testit
import allure
from playwright.sync_api import expect

from page_objects.header_element import HeaderElement


@allure.title("Переход на страницу 'Статьи'")
def test_header_link_blogs(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        with page_fixture.expect_popup() as page1_info:
            page_fixture.get_by_role("link", name="Статьи", exact=True).click()
    with allure.step("Дожидаюсь открытия страницы"):
        page1 = page1_info.value
        page1.wait_for_url(re.compile('blogs'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page1).to_have_url(re.compile('blogs'))
    with allure.step("Проверяю, что статус страницы ok"):
        response = page1.request.get(page1.url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Бренды'")
def test_header_link_brands(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.get_by_role("banner").get_by_role("link", name="Бренды").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(re.compile('brands'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(re.compile('brands'))
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Магазины'")
def test_header_link_contacts(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        with page_fixture.expect_popup() as page1_info:
            page_fixture.get_by_role("link", name="Магазины").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page1 = page1_info.value
        page1.wait_for_load_state("domcontentloaded")
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page1).to_have_url(re.compile('contacts'))
    with allure.step("Проверяю, что статус страницы ok"):
        response = page1.request.get(page1.url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Доставка и оплата'")
def test_header_link_dostavka_oplata(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.get_by_role("banner").get_by_role("link", name="Доставка и оплата").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(re.compile('dostavka-oplata'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(re.compile('dostavka-oplata'))
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на домашнюю страницу")
# @testit.workItemIds("184") # ручной
# @testit.externalID("137583ce6919fca3ae3d379bc6a5007849e6853ff907b7610f761fa8131db009") # авто 169
# @pytest.mark.test_for_ci
def test_test_header_link_home(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.wait_for_url(f'{base_url}/')
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(f'{base_url}/')
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(f'{base_url}/')
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Как сделать заказ'")
def test_header_link_how_to_order(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.get_by_role("banner").get_by_role("link", name="Как сделать заказ").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(re.compile('how-to-order'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(re.compile('how-to-order'))
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Круг друзей'")
def test_header_link_krug(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.get_by_role("banner").get_by_role("link", name="Круг друзей").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(re.compile('krug'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(re.compile('krug'))
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Новости'")
def test_header_link_news(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.get_by_role("banner").get_by_role("link", name="Новости").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(re.compile('news'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(re.compile('news'))
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Акции'")
def test_header_link_promos(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        page_fixture.get_by_role("banner").get_by_role("link", name="Акции").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page_fixture.wait_for_url(re.compile('promos'))
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page_fixture).to_have_url(re.compile('promos'))
    with allure.step("Проверяю, что статус страницы ok"):
        url = page_fixture.url
        response = page_fixture.request.get(url)
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Видео-обзоры'")
def test_header_link_video_reviews(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        with page_fixture.expect_popup() as page1_info:
            page_fixture.get_by_role("banner").get_by_role("link", name="Видео-обзоры").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page1 = page1_info.value
        page1.wait_for_load_state("domcontentloaded")
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page1).to_have_url(re.compile('26252490'))
    with allure.step("Проверяю, что статус страницы ok"):
        response = page1.request.get('https://rutube.ru/channel/26252490')
        expect(response).to_be_ok()


@allure.title("Переход на страницу 'Гарантии'")
def header_link_warranty(page_fixture, base_url):
    header = HeaderElement(page_fixture)
    header.open(base_url)
    with allure.step("Кликаю на ссылку"):
        with page_fixture.expect_popup() as page1_info:
            page_fixture.get_by_role("banner").get_by_role("link", name="Гарантии").click()
    with allure.step("Дожидаюсь открытия страницы"):
        page1 = page1_info.value
        page1.wait_for_load_state("domcontentloaded")
    with allure.step("Проверяю, что url страницы содержит требуемое значение"):
        expect(page1).to_have_url(re.compile('warranty'))
    with allure.step("Проверяю, что статус страницы ok"):
        response = page1.request.get(page1.url)
        expect(response).to_be_ok()



# def test_home(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.wait_for_url(f'{url}')
#     expect(page).to_have_url(f'{url}')
#     response = page.request.get(f'{url}')
#     expect(response).to_be_ok()
#
# def test_header_link(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.get_by_role("banner").get_by_role("link", name="Новости").click()
#     page.wait_for_url(f'{url}gt/news')
#     expect(page).to_have_url(f'{url}gt/news')
#     response = page.request.get(f'{url}gt/news')
#     expect(response).to_be_ok()
#
# def test_header_link1(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.get_by_role("banner").get_by_role("link", name="Круг друзей").click()
#     page.wait_for_url(f'{url}krug')
#     expect(page).to_have_url(f'{url}krug')
#     response = page.request.get(f'{url}krug')
#     expect(response).to_be_ok()
#
# def test_header_link2(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.get_by_role("banner").get_by_role("link", name="Доставка и оплата").click()
#     page.wait_for_url(f'{url}dostavka-oplata')
#     expect(page).to_have_url(f'{url}dostavka-oplata')
#     response = page.request.get(f'{url}dostavka-oplata')
#     expect(response).to_be_ok()
#
#
# def test_header_link(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.get_by_role("banner").get_by_role("link", name="Гарантии").click()
#     page.wait_for_url(f'{url}warranty')
#     expect(page).to_have_url(f'{url}warranty')
#     response = page.request.get(f'{url}warranty')
#     expect(response).to_be_ok()
#
# def test_header_link(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.get_by_role("banner").get_by_role("link", name="Как сделать заказ").click()
#     page.wait_for_url(f'{url}how-to-order')
#     expect(page).to_have_url(f'{url}how-to-order')
#     response = page.request.get(f'{url}how-to-order')
#     expect(response).to_be_ok()
#
#
# def test_header_link(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     page.get_by_role("link", name="Магазины").click()
#     page.wait_for_url(f'{url}contacts')
#     expect(page).to_have_url(f'{url}contacts')
#     response = page.request.get(f'{url}contacts')
#     expect(response).to_be_ok()
#
# def test_header_link(page):
#     url = "https://garwin.ru/"                                              # Вводим переменную
#     page.goto(f'{url}', wait_until='domcontentloaded')                      # Переход на домашнюю страницу, ожидаем загрузку DOM-дерева
#     page.get_by_role("banner").get_by_role("link", name="Бренды").click()   # Кликаем на ссылку
#     page.wait_for_url(f'{url}brands')                                       # Ожидаем когда URL будет соответствовать заданному
#     expect(page).to_have_url(f'{url}brands')                                # Проверяем, что URL осответствует заданному
#     response = page.request.get(f'{url}brands')                             # Отправляем гет запрос, заводим переменную
#     expect(response).to_be_ok()                                                 # Проверяем, что статус код переменной - ok

# def test_header_link(page):
#     url = "https://garwin.ru/"
#     page.goto(f'{url}', wait_until='domcontentloaded')
#     with page.expect_popup() as page1_info:
#         page.get_by_role("banner").get_by_role("link", name="Видео-обзоры").click()
#     page1 = page1_info.value
#     page1.wait_for_url(re.compile('@garwin_tools'))
#     expect(page1).to_have_url(re.compile('@garwin_tools'))
#     response = page.request.get('https://www.youtube.com/@garwin_tools')
#     expect(response).to_be_ok()

# testit.workItemIds - linking an autotest to a test case
# @testit.displayName("Это пробное название теста")
# testit.externalId - ID of the autotest within the project in the Test IT System
# testit.title - title in the autotest card
# testit.description - description in the autotest card
# testit.labels - tags in the work item
# testit.links - links in the autotest card
# testit.namespace - directory in the TMS system (default - directory's name of test)
# testit.classname - subdirectory in the TMS system (default - file's name of test)
