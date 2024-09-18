import re
import pytest
from playwright.sync_api import expect


@pytest.mark.test_for_ci
def test_home(page_fixture):
    url = "https://garwin.ru/"
    page_fixture.goto(f'{url}', wait_until='domcontentloaded')
    page_fixture.wait_for_url(f'{url}')
    expect(page_fixture).to_have_url(f'{url}')
    response = page_fixture.request.get(f'{url}')
    expect(response).to_be_ok()