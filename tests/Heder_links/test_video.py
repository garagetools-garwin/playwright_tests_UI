import re

from playwright.sync_api import expect


def test_header_link(page_fixture, base_url):
    page_fixture.goto(f'{base_url}', wait_until='domcontentloaded')
    with page_fixture.expect_popup() as page1_info:
        page_fixture.get_by_role("banner").get_by_role("link", name="Видео-обзоры").click()
    page1 = page1_info.value
    page1.wait_for_url(re.compile('@garwin_tools'))
    expect(page1).to_have_url(re.compile('@garwin_tools'))
    response = page_fixture.request.get('https://www.youtube.com/@garwin_tools')
    expect(response).to_be_ok()