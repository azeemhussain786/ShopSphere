"""
ShopSphere Page Object Model - HomePage Class
Encapsulates all locators, actions, and validations on the ShopSphere homepage.
"""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for the ShopSphere Homepage."""

    # ==========================================
    # Locators (Actual DOM selectors)
    # ==========================================
    BODY = (By.ID, "shopsphere-body")
    BRAND_LOGO = (By.ID, "brand-logo")
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BTN = (By.ID, "search-btn")
    NAV_CART_BTN = (By.ID, "nav-cart-btn")
    CART_COUNT_BADGE = (By.ID, "cart-count")
    TOAST_CONTAINER = (By.ID, "notification-toast")
    TOAST_MESSAGE = (By.ID, "toast-message")
    HERO_TITLE = (By.ID, "hero-title")
    HERO_SHOP_BTN = (By.ID, "hero-shop-btn")
    SORT_SELECT = (By.ID, "sort-select")
    CATEGORY_FILTER_BAR = (By.ID, "category-filter-bar")
    PRODUCT_COUNT = (By.ID, "product-count")
    PRODUCTS_GRID = (By.ID, "products-grid")
    NO_PRODUCTS_MSG = (By.ID, "no-products-msg")

    # CSS Selectors for Product Elements
    VISIBLE_PRODUCT_CARDS = (By.CSS_SELECTOR, "#products-grid .product-card:not(.hidden)")
    VISIBLE_PRODUCT_TITLES = (By.CSS_SELECTOR, "#products-grid .product-card:not(.hidden) .product-title")
    VISIBLE_PRODUCT_PRICES = (By.CSS_SELECTOR, "#products-grid .product-card:not(.hidden) .current-price")

    def __init__(self, driver, base_url: str = "http://127.0.0.1:5000"):
        super().__init__(driver)
        self.base_url = base_url

    def load(self) -> "HomePage":
        """Navigates to the ShopSphere homepage and waits for the body to be visible."""
        self.driver.get(self.base_url)
        self.wait_for_element_visible(self.BODY)
        return self

    def get_brand_logo_text(self) -> str:
        """Returns the text of the brand logo."""
        return self.get_text(self.BRAND_LOGO)

    def get_hero_title_text(self) -> str:
        """Returns the text of the hero title."""
        return self.get_text(self.HERO_TITLE)

    def search_product(self, keyword: str) -> "HomePage":
        """Types a keyword into the search input and triggers search."""
        self.type_text(self.SEARCH_INPUT, keyword)
        return self

    def clear_search(self) -> "HomePage":
        """Clears the search input field."""
        search_elem = self.wait_for_element_visible(self.SEARCH_INPUT)
        search_elem.clear()
        # Trigger event by sending backspace
        search_elem.send_keys("a")
        search_elem.clear()
        return self

    def filter_by_category(self, category_name: str) -> "HomePage":
        """Clicks a category pill matching the given category name."""
        cat_locator = (By.CSS_SELECTOR, f".filter-pill[data-category='{category_name}']")
        self.click(cat_locator)
        return self

    def sort_by(self, sort_value: str) -> "HomePage":
        """
        Selects a sort option from the dropdown.
        Allowed sort_values: 'default', 'price-low', 'price-high', 'rating-high'.
        """
        select_element = self.wait_for_element_visible(self.SORT_SELECT)
        dropdown = Select(select_element)
        dropdown.select_by_value(sort_value)
        return self

    def get_product_count_text(self) -> str:
        """Returns the status text from the product count bar (e.g. 'Showing 18 products')."""
        return self.get_text(self.PRODUCT_COUNT)

    def get_visible_product_cards(self) -> list:
        """Returns a list of currently visible product card WebElements."""
        return self.find_elements(self.VISIBLE_PRODUCT_CARDS)

    def get_visible_product_count(self) -> int:
        """Returns the number of product cards currently visible on the grid."""
        return len(self.get_visible_product_cards())

    def get_visible_product_titles(self) -> List[str]:
        """Returns a list of titles of all currently visible products."""
        elements = self.find_elements(self.VISIBLE_PRODUCT_TITLES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_visible_product_prices(self) -> List[float]:
        """
        Extracts and parses all currently visible product prices as numeric floats.
        Strips currency symbols (₹) and thousands separator commas.
        """
        elements = self.find_elements(self.VISIBLE_PRODUCT_PRICES)
        prices = []
        for el in elements:
            raw_text = el.text.strip()
            # Remove '₹' and ',' then parse as float
            cleaned = raw_text.replace("₹", "").replace(",", "").strip()
            if cleaned:
                prices.append(float(cleaned))
        return prices

    def add_product_to_cart_by_id(self, product_id: int) -> "HomePage":
        """Clicks the 'Add to Cart' button for a specific product ID."""
        btn_locator = (By.ID, f"add-to-cart-{product_id}")
        self.click(btn_locator)
        return self

    def get_cart_badge_count(self) -> int:
        """Reads and parses the numerical cart badge counter in the top navigation."""
        badge_text = self.get_text(self.CART_COUNT_BADGE)
        return int(badge_text) if badge_text.isdigit() else 0

    def get_toast_message(self) -> str:
        """Waits for and returns the text displayed in the toast notification."""
        return self.get_text(self.TOAST_MESSAGE)

    def open_cart_drawer(self) -> "HomePage":
        """Clicks the navbar cart button to slide open the cart drawer."""
        self.click(self.NAV_CART_BTN)
        return self
