from playwright.sync_api import expect


def test_header_link(page):
    # Переходим на главную страницу
    page.goto("https://garwin.ru/", wait_until='domcontentloaded')

    # Проверяем, что URL соответствует ожидаемому
    expect(page).to_have_url("https://garwin.ru/")

    # Отправляем GET-запрос и проверяем, что ответ OK
    response_home = page.request.get('https://garwin.ru/')
    expect(response_home).to_be_ok()

    # Кликаем на ссылку "Акции"
    page.get_by_role("banner").get_by_role("link", name="Акции").click(force=True)

    # Отправляем GET-запрос для новой страницы и проверяем, что ответ OK
    response_actions = page.request.get('https://garwin.ru/gt/news')
    expect(response_actions).to_be_ok()

    # Кликаем на ссылку "Новости"
    page.get_by_role("banner").get_by_role("link", name="Новости").click(force=True)

    # Ожидаем загрузки страницы полностью после клика
    page.wait_for_load_state("load")

    # Выводим текущий URL перед и после клика
    print("URL before click:", page.url)

    # Получаем текущий URL и проверяем, что он соответствует ожидаемому
    current_url = page.url
    print(page.url)

    assert current_url == "https://garwin.ru/gt/news"
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
