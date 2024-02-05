from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru"
    response = page.request.get(f'{url}/promos')
    expect(response).to_be_ok()
    print(response.status)
    response = page.request.get(f'{url}/gt/news')
    expect(response).to_be_ok()
    print(response.status)
    response = page.request.get(f'{url}/krug')
    expect(response).to_be_ok()
    response = page.request.get(f'{url}/dostavka-oplata')
    expect(response).to_be_ok()
    response = page.request.get(f'{url}/warranty')
    expect(response).to_be_ok()
    response = page.request.get(f'{url}/how-to-order')
    expect(response).to_be_ok()
    response = page.request.get(f'{url}/contacts')
    expect(response).to_be_ok()
    response = page.request.get(f'{url}/brands')
    expect(response).to_be_ok()
    response = page.request.get('https://blogs.garwin.ru/')
    expect(response).not_to_be_ok()
    response = page.request.get('https://www.youtube.com/@garwin_tools')
    expect(response).to_be_ok()
