import re

from playwright.sync_api import expect


def test_header_link2(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("banner").get_by_role("link", name="Доставка и оплата").click()
    page.wait_for_url(f'{url}dostavka-oplata')
    expect(page).to_have_url(f'{url}dostavka-oplata')
    response = page.request.get(f'{url}dostavka-oplata')
    expect(response).to_be_ok()