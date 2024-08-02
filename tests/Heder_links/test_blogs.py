import re
import testit
from playwright.sync_api import expect


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
@testit.displayName("Это пробное название теста")
# testit.externalId - ID of the autotest within the project in the Test IT System
# testit.title - title in the autotest card
# testit.description - description in the autotest card
# testit.labels - tags in the work item
# testit.links - links in the autotest card
# testit.namespace - directory in the TMS system (default - directory's name of test)
# testit.classname - subdirectory in the TMS system (default - file's name of test)
def test_header_link(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Статьи", exact=True).click()
    page1 = page1_info.value
    page1.wait_for_url(re.compile('https://blogs.garwin.ru/'))
    expect(page1).to_have_url(re.compile('https://blogs.garwin.ru/'))
    response = page1.request.get('https://blogs.garwin.ru/')
    expect(response).to_be_ok()




