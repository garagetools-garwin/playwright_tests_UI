def test_inventory(page):
    response = page.request.get('https://garwin.ru/promos')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://garwin.ru/gt/news')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://garwin.ru/krug')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://garwin.ru/dostavka-oplata')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://garwin.ru/how-to-order')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://garwin.ru/brands')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://blogs.garwin.ru/?_ga=2.162138428.1609255590.1706176410-1714696286.1706176410')
    assert response.status == 200
    print(response.status)
    response = page.request.get('https://www.youtube.com/@garwin_tools')
    assert response.status == 200
    print("Статус", response.status)
