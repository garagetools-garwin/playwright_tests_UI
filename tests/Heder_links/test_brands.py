import re

from playwright.sync_api import expect


def test_header_link(page_fixture):
    url = "https://garwin.ru/"                                              # Вводим переменную
    page_fixture.goto(f'{url}', wait_until='domcontentloaded')                      # Переход на домашнюю страницу, ожидаем загрузку DOM-дерева
    page_fixture.get_by_role("banner").get_by_role("link", name="Бренды").click()   # Кликаем на ссылку
    page_fixture.wait_for_url(f'{url}brands')                                       # Ожидаем когда URL будет соответствовать заданному
    expect(page_fixture).to_have_url(f'{url}brands')                                # Проверяем, что URL осответствует заданному
    response = page_fixture.request.get(f'{url}brands')                             # Отправляем гет запрос, заводим переменную
    expect(response).to_be_ok()                                                 # Проверяем, что статус код переменной - ok