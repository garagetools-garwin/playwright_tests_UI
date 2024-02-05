from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.webkit.launch()
    context = browser.new_context()
    page = context.new_page()

    # Ваши действия с веб-страницей

    browser.close()