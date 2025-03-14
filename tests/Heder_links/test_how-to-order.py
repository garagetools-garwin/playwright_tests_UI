import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect

# with sync_playwright() as p:
#     browser = p.chromium.launch(channel="chrome")


def test_header_link(page_fixture, base_url):
    page_fixture.goto(f'{base_url}', wait_until='domcontentloaded')
    page_fixture.get_by_role("banner").get_by_role("link", name="Как сделать заказ").click()
    page_fixture.wait_for_url(f'{base_url}/how-to-order')
    expect(page_fixture).to_have_url(f'{base_url}/how-to-order')
    response = page_fixture.request.get(f'{base_url}/how-to-order')
    expect(response).to_be_ok()