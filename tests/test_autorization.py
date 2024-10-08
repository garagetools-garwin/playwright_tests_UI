import os
import re
import time
import allure
import requests

from playwright.sync_api import expect
import pytest
from page_objects.autorization_modal_element import AutorizationModalElement

url = "https://garwin.ru"

"""Этот тест проверяет работу авторизации"""


@pytest.mark.skip("Пропущен для экономии отправленых сообщения, авторизация проходит в тесте'Переход в чек-аут'")
@allure.title("Авторизуюсь через testmail.app")
def test_autorization_code_testmail_app(page_fixture, base_url):
    autorization = AutorizationModalElement(page_fixture)
    page_fixture.goto(f'{url}')
    page_fixture.locator(".NavigationButton__Overlay.NavigationButtonOverlay").nth(0).click()
    autorization.cart_autorization_send_code_testmail_app()
    code = autorization.get_autorization_code_testmail_app()
    autorization.complete_autorization(code)
    username = page_fixture.locator("p.NavigationButton__Text").nth(1).inner_text()
    with allure.step("Проверяю, что имя пользователя отображается в хедере"):
        assert username == "Test Test"
    page_fixture.context.storage_state(path="auth_state.json")


@allure.title("Авторизация через mail.ru")
@pytest.mark.skip("Архив. mail.ru бокирует запуск в CI по тому что идет обращения с разных IP, тест можно использовать локально")
def autorization_mail_ru(page_fixture):
    autorization = AutorizationModalElement(page_fixture)
    page_fixture.goto("https://account.mail.ru")
    # page.locator("resplash-btn.resplash-btn_primary.resplash-btn_mailbox-big.icjbjfg-10hc17k").click()
    page_fixture.locator('[name="username"]').fill("testgarwin_yur@mail.ru")
    page_fixture.locator('[data-test-id="next-button"]').click()
    page_fixture.locator('[type="password"]').fill("")
    page_fixture.locator('[data-test-id="submit-button"]').click()
    page_fixture.get_by_text("Авторизация на сайте Гарвин").nth(0).click()
    code = page_fixture.locator('span[style="font-weight:bold;"]').inner_text()
    autorization.complete_autorization(code)
    username = page_fixture.locator("p.NavigationButton__Text").nth(1).inner_text()
    with allure.step("Проверяю, что имя пользователя отображается в хедере"):
        assert username == "Test Test"
    page_fixture.context.storage_state(path="auth_state.json")
    print(code)


"""Архив"""


@pytest.mark.skip("Архив")
@allure.title("Авторизация с паролем (Архив)")
def autorization_archive(page):
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


@pytest.mark.skip("Гугл блокирует автоматизированную авторизацию")
@allure.title("Авторизация через gmail")
def autorization_google(page):
    page.goto("https://www.google.com/intl/en-US/gmail/about/")
    page.get_by_text("Sign in").click()
    page.locator("#identifierId").fill("testgarwin@gmail.com")
    page.locator(".VfPpkd-vQzf8d").nth(1).click()
    time.sleep(5)
    page.locator(".whsOnd.zHQkBf").fill("MuIPU&iasb21")
    page.locator(".VfPpkd-vQzf8d").nth(1).click()
    page.get_by_text("Авторизация на сайте Гарвин").nth(0).click()


"""Тесты для настройки авторизации на stage"""


@pytest.mark.skip("Тест еще в разработке")
def stage_login(page):
    page.goto('https://stage.garagetools.ru/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd')

    # Optionally, you can add assertions here to verify successful login
    assert page.url == 'https://stage.garagetools.ru/expected_page_after_login'


@pytest.mark.skip("Тест еще в разработке")
def stage_login_1(page):
    page.goto('https://stage.garagetools.ru/tovar/sverlo-spiralnoe-po-metallu-50-mm-hss-g-din338-5xd')

    # Optionally, you can add assertions here to verify successful login
    assert page.url == 'https://stage.garagetools.ru/expected_page_after_login'


@pytest.mark.skip("Тест еще в разработке")
def stage_login_2(page):
    page.goto('https://stage.garagetools.ru')

    # Fill in the username and password fields
    page.fill('input[name="username"]', 'garage')
    page.fill('input[name="password"]', 'cYZcgPPf')

    # Click the login button
    page.click('button[type="submit"]')

    # Optionally, you can add assertions here to verify successful login
    assert page.url == 'https://stage.garagetools.ru/expected_page_after_login'


