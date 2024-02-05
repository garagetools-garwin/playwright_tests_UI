import re

from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("link", name="Магазины").click()
    page.wait_for_url(f'{url}contacts')
    expect(page).to_have_url(f'{url}contacts')
    response = page.request.get(f'{url}contacts')
    expect(response).to_be_ok()