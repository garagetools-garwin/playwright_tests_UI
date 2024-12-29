import re

from playwright.sync_api import expect


def test_header_link2(page_fixture, base_url):
    page_fixture.goto(f'{base_url}', wait_until='domcontentloaded')
    page_fixture.get_by_role("banner").get_by_role("link", name="Доставка и оплата").click()
    page_fixture.wait_for_url(f'{base_url}dostavka-oplata')
    expect(page_fixture).to_have_url(f'{base_url}dostavka-oplata')
    response = page_fixture.request.get(f'{base_url}dostavka-oplata')
    expect(response).to_be_ok()