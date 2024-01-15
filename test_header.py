from playwright.sync_api import expect

def test_header_link(page):
    page.goto("https://garwin.ru/", wait_until='domcontentloaded')
    expect(page).to_have_url("https://garwin.ru/")
    response = page.request.get('https://garwin.ru/')
    expect(response).not_to_be_ok
    page.get_by_role("banner").get_by_role("link", name="Акции").click(force=True)
    page.get_by_role("banner").get_by_role("link", name="Новости").click(force=True)
    page.get_by_role("banner").get_by_role("link", name="Круг друзей").click()
    page.get_by_role("banner").get_by_role("link", name="Доставка и оплата").click()
    page.get_by_role("banner").get_by_role("link", name="Гарантии").click()
    page.get_by_role("banner").get_by_role("link", name="Как сделать заказ").click()
    page.get_by_role("link", name="Магазины").click()
    page.get_by_role("banner").get_by_role("link", name="Бренды").click()
    page.get_by_role("link", name="Статьи", exact=True).click()
    page.goto("https://garwin.ru/brands")
    with page.expect_popup() as page1_info:
        page.get_by_role("banner").get_by_role("link", name="Видео-обзоры").click()
    page1 = page1_info.value

