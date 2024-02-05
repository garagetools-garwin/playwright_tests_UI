from playwright.sync_api import expect


def test_header_link(page):
    url = "https://garwin.ru/"
    page.goto(f'{url}', wait_until='domcontentloaded')
    page.get_by_role("banner").get_by_role("link", name="Акции").click()
    page.wait_for_url(f'{url}/promos')
    current_url = page.url
    assert current_url == f'{url}/promos'
    response = page.request.get(f'{url}/promos')
    expect(response).to_be_ok()
    page.get_by_role("banner").get_by_role("link", name="Новости").click()
    page.wait_for_url(f'{url}/gt/news')
    current_url = page.url
    assert current_url == f'{url}/gt/news'
    response = page.request.get(f'{url}/gt/news')
    expect(response).to_be_ok()
    page.get_by_role("banner").get_by_role("link", name="Круг друзей").click()
    page.wait_for_url(f'{url}/krug')
    current_url = page.url
    assert current_url == f'{url}/krug'
    response = page.request.get(f'{url}/krug')
    expect(response).to_be_ok()
    page.get_by_role("banner").get_by_role("link", name="Доставка и оплата").click()
    page.wait_for_url(f'{url}/dostavka-oplata')
    current_url = page.url
    assert current_url == f'{url}/dostavka-oplata'
    response = page.request.get(f'{url}/dostavka-oplata')
    expect(response).to_be_ok()
    page.get_by_role("banner").get_by_role("link", name="Гарантии").click()
    page.wait_for_url(f'{url}/warranty')
    current_url = page.url
    assert current_url == f'{url}/warranty'
    response = page.request.get(f'{url}/warranty')
    expect(response).to_be_ok()
    page.get_by_role("banner").get_by_role("link", name="Как сделать заказ").click()
    page.wait_for_url(f'{url}/how-to-order')
    current_url = page.url
    assert current_url == f'{url}/how-to-order'
    response = page.request.get(f'{url}/how-to-order')
    expect(response).to_be_ok()
    page.get_by_role("link", name="Магазины").click()
    page.wait_for_url(f'{url}/contacts')
    current_url = page.url
    assert current_url == f'{url}/contacts'
    response = page.request.get(f'{url}/contacts')
    expect(response).to_be_ok()
    page.get_by_role("banner").get_by_role("link", name="Бренды").click()
    page.wait_for_url(f'{url}/brands')
    current_url = page.url
    assert current_url == f'{url}/brands'
    response = page.request.get(f'{url}/brands')
    expect(response).to_be_ok()
    page.get_by_role("link", name="Статьи", exact=True).click()
    response = page.request.get('https://blogs.garwin.ru/')
    expect(response).to_be_ok()
    page.goto("https://garwin.ru/brands")
    with page.expect_popup() as page1_info:
        page.get_by_role("banner").get_by_role("link", name="Видео-обзоры").click()
    page1 = page1_info.value
    page.wait_for_url('https://www.youtube.com/@garwin_tools')
    current_url = page.url
    assert current_url == 'https://www.youtube.com/@garwin_tools'
    response = page.request.get('https://www.youtube.com/@garwin_tools')
    expect(response).to_be_ok()
