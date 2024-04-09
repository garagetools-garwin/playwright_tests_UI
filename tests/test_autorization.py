import re
from playwright.sync_api import expect
import pytest

url = "https://garwin.ru"

"""Этот тест проверяет работу авторизации"""


@pytest.mark.smoke
@pytest.mark.regress
def test_autorization(page):
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(0).click()
    page.locator("input[type=\"email\"]").click()
    page.locator("input[type=\"email\"]").fill("testgarwin@gmail.com")
    page.locator("input[type=\"password\"]").click()
    page.locator("input[type=\"password\"]").fill("12345")
    page.get_by_role("button", name="Войти").click()
    locator = (
        page.get_by_role("banner")
        .locator("div")
        .filter(has_text=re.compile(r"^test_num$"))
        .get_by_role("paragraph")
    )
    # Проверяем, что иконка профиля содержит нужный нам текст
    expect(locator).to_have_text("test_num")
    page.get_by_role("banner").locator("div").filter(has_text=re.compile(r"^test_num$")).click()
    locator2 = page.get_by_role("button", name="test_num")
    # Проверяем, что имя профиля на странице профиля содержит нужный нам текст
    expect(locator2).to_have_text("test_num")
