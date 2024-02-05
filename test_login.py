
def test_header_link(page):
    page.goto('https://automationexercise.com/login', wait_until="domcontentloaded")
    with page.expect_response("https://automationexercise.com/login") as response_info:
        page.locator('[data-qa="login-email"]').fill("asd@f.rf")
        page.locator('[data-qa="login-password"]').fill("a")
        page.locator('[data-qa="login-button"]').click()
        response = response_info.value
        assert response.status == 200
