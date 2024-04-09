import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")


def test_header_link(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("banner").get_by_role("link", name="Как сделать заказ").click()
    page.wait_for_url(f'{url}how-to-order')
    expect(page).to_have_url(f'{url}how-to-order')
    response = page.request.get(f'{url}how-to-order')
    expect(response).to_be_ok()