import re

from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("banner").get_by_role("link", name="Новости").click()
    page.wait_for_url(f'{url}gt/news')
    expect(page).to_have_url(f'{url}gt/news')
    response = page.request.get(f'{url}gt/news')
    expect(response).to_be_ok()