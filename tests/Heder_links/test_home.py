import re

from playwright.sync_api import expect


def test_home(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.wait_for_url(f'{url}')
    expect(page).to_have_url(f'{url}')
    response = page.request.get(f'{url}')
    expect(response).to_be_ok()