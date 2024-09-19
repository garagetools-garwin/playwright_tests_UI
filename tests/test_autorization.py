import re
import time
import allure

from playwright.sync_api import expect
import pytest

url = "https://garwin.ru"

"""Этот тест проверяет работу авторизации"""


@allure.title("Авторизация через mail.ru")
def test_autorization_mail_ru(page_fixture):
    page_fixture.goto("https://account.mail.ru")
    # page.locator("resplash-btn.resplash-btn_primary.resplash-btn_mailbox-big.icjbjfg-10hc17k").click()
    page_fixture.locator('[name="username"]').fill("testgarwin_yur@mail.ru")
    page_fixture.locator('[data-test-id="next-button"]').click()
    page_fixture.locator('[type="password"]').fill("MuIPU&iasb21")
    page_fixture.locator('[data-test-id="submit-button"]').click()
    page_fixture.get_by_text("Авторизация на сайте Гарвин").nth(0).click()
    code = page_fixture.locator('span[style="font-weight:bold;"]').inner_text()
    print(code)


"""Архив"""


@pytest.mark.skip("Архив")
@allure.title("Авторизация (Архив)")
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


