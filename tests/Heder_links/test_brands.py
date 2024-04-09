import re

from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru/"                                              # Вводим переменную
    page.goto(f'{url}', wait_until='domcontentloaded')                      # Переход на домашнюю страницу, ожидаем загрузку DOM-дерева
    page.get_by_role("banner").get_by_role("link", name="Бренды").click()   # Кликаем на ссылку
    page.wait_for_url(f'{url}brands')                                       # Ожидаем когда URL будет соответствовать заданному
    expect(page).to_have_url(f'{url}brands')                                # Проверяем, что URL осответствует заданному
    response = page.request.get(f'{url}brands')                             # Отправляем гет запрос, заводим переменную
    expect(response).to_be_ok()                                                 # Проверяем, что статус код переменной - ok