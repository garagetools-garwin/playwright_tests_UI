import re

from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru/"
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("link", name="Статьи", exact=True).click()
    page.wait_for_url(re.compile('https://blogs.garwin.ru/'))
    expect(page).to_have_url(re.compile('https://blogs.garwin.ru/'))
    response = page.request.get('https://blogs.garwin.ru/')
    expect(response).to_be_ok()
    #fffff