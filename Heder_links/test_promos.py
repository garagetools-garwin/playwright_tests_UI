import re

from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("banner").get_by_role("link", name="Акции").click()
    page.wait_for_url(f'{url}promos')
    expect(page).to_have_url(f'{url}promos')
    response = page.request.get(f'{url}promos')
    expect(response).to_be_ok()