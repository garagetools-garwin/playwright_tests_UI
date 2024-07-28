"""
На данный момент фреймворк не подразумевает использование BasePage. Код ниже предполагает, что:
1) Можно будет убрать инициализацию из всех остальных страниц
2) Можно будет заменить привычную конструкцию self.page.locator(selector) на get_element
"""

# class BasePage:
#     def __init__(self, page):
#         self.page = page
#
#     def get_element(self, selector: str, timeout=3000):
#         """
#         Waits for the element to be visible and returns it.
#         :param selector: The selector of the element to find.
#         :param timeout: The maximum time to wait for the element (in milliseconds).
#         :return: The located element.
#         """
#         self.page.wait_for_selector(selector, state='visible', timeout=timeout)
#         return self.page.locator(selector)