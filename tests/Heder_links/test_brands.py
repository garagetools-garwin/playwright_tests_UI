import re

from playwright.sync_api import expect


def test_header_link(page_fixture, base_url):                                          # Вводим переменную
    page_fixture.goto(f'{base_url}', wait_until='domcontentloaded')                      # Переход на домашнюю страницу, ожидаем загрузку DOM-дерева
    page_fixture.get_by_role("banner").get_by_role("link", name="Бренды").click()   # Кликаем на ссылку
    page_fixture.wait_for_url(f'{base_url}/brands')                                       # Ожидаем когда URL будет соответствовать заданному
    expect(page_fixture).to_have_url(f'{base_url}/brands')                                # Проверяем, что URL осответствует заданному
    response = page_fixture.request.get(f'{base_url}/brands')                             # Отправляем гет запрос, заводим переменную
    expect(response).to_be_ok()                                                 # Проверяем, что статус код переменной - ok