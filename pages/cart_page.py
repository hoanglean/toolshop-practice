from pages.base_page import BasePage


def money(text: str) -> float:
    """'$28.30' -> 28.3"""
    return float(text.replace("$", "").replace(",", "").strip())


class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)
        self.product_titles = page.get_by_test_id("product-title")
        self.quantities = page.get_by_test_id("product-quantity")
        self.line_prices = page.get_by_test_id("line-price")
        self.total = page.get_by_test_id("cart-total")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    def line_totals(self) -> list[float]:
        return [money(text) for text in self.line_prices.all_inner_texts()]

    def total_value(self) -> float:
        return money(self.total.inner_text())

    def continue_shopping(self):
        from pages.home_page import HomePage

        self.continue_shopping_button.click()
        return HomePage(self.page)
