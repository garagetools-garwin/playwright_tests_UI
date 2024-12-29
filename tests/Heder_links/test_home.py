import re
import testit
import allure
import pytest
from playwright.sync_api import expect

@allure.title("Переход на домашнюю страницу")
@testit.workItemIds("184") # ручной
@testit.externalID("137583ce6919fca3ae3d379bc6a5007849e6853ff907b7610f761fa8131db009") # авто 169
@pytest.mark.test_for_ci
def test_home(page_fixture, base_url):
    page_fixture.goto(f'{base_url}/', wait_until='domcontentloaded')
    page_fixture.wait_for_url(f'{base_url}/')
    expect(page_fixture).to_have_url(f'{base_url}/')
    response = page_fixture.request.get(f'{base_url}/')
    expect(response).to_be_ok()
