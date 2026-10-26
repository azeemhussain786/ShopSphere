"""
ShopSphere Page Object Model - CartDrawer Class
Encapsulates all locators, state queries, and user actions on the Cart Drawer.
"""

from typing import Optional
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartDrawer(BasePage):
    """Page Object representing the sliding Shopping Cart Drawer."""

    # ==========================================
    # Locators (Actual DOM selectors)
    # ==========================================
    DRAWER = (By.ID, "cart-drawer")
    BACKDROP = (By.ID, "cart-backdrop")
    CLOSE_BTN = (By.ID, "cart-close-btn")
    HEADER_TITLE = (By.ID, "cart-title")
    ITEMS_TOTAL_BADGE = (By.ID, "cart-items-total-badge")
    EMPTY_STATE = (By.ID, "cart-empty-state")
    START_SHOPPING_BTN = (By.ID, "cart-start-shopping-btn")
    ITEMS_CONTAINER = (By.ID, "cart-items-container")
    DRAWER_FOOTER = (By.ID, "cart-drawer-footer")
    SUBTOTAL = (By.ID, "cart-subtotal")
    TOTAL = (By.ID, "cart-total")
    CHECKOUT_BTN = (By.ID, "cart-checkout-btn")
    CHECKOUT_MODAL = (By.ID, "checkout-modal")
    TOAST_MESSAGE = (By.ID, "toast-message")

    def is_drawer_open(self, timeout: int = 5) -> bool:
        """
        Verifies whether the cart drawer is currently open and visible.
        Checks both the CSS 'open' class on the drawer element and its visibility.
        """
        try:
            drawer_elem = self.wait_for_element_visible(self.DRAWER, timeout=timeout)
            classes = drawer_elem.get_attribute("class") or ""
            return "open" in classes.split()
        except Exception:
            return False

    def close(self) -> None:
        """Clicks the close button on the cart drawer."""
        self.click(self.CLOSE_BTN)

    def is_empty_state_visible(self) -> bool:
        """Checks if the empty cart illustration/message is displayed."""
        return self.is_visible(self.EMPTY_STATE)

    def get_subtotal_amount(self) -> float:
        """
        Reads and parses the cart subtotal as a float.
        Converts '₹4,999' into 4999.0.
        """
        raw_text = self.get_text(self.SUBTOTAL)
        cleaned = raw_text.replace("₹", "").replace(",", "").strip()
        return float(cleaned) if cleaned else 0.0

    def get_total_amount(self) -> float:
        """
        Reads and parses the grand total amount as a float.
        Converts '₹4,999' into 4999.0.
        """
        raw_text = self.get_text(self.TOTAL)
        cleaned = raw_text.replace("₹", "").replace(",", "").strip()
        return float(cleaned) if cleaned else 0.0

    def get_item_quantity(self, product_id: int) -> int:
        """Reads the current quantity stepper value for a specific product ID."""
        qty_locator = (By.ID, f"qty-val-{product_id}")
        qty_text = self.get_text(qty_locator)
        return int(qty_text) if qty_text.isdigit() else 0

    def get_item_subtotal(self, product_id: int) -> float:
        """Reads and parses the subtotal amount for a specific product line item."""
        subtotal_locator = (By.ID, f"cart-item-subtotal-{product_id}")
        raw_text = self.get_text(subtotal_locator)
        cleaned = raw_text.replace("₹", "").replace(",", "").strip()
        return float(cleaned) if cleaned else 0.0

    def increase_quantity(self, product_id: int) -> None:
        """Clicks the '+' button to increment the quantity for a product."""
        plus_locator = (By.ID, f"qty-plus-{product_id}")
        self.click(plus_locator)

    def decrease_quantity(self, product_id: int) -> None:
        """Clicks the '-' button to decrement the quantity for a product."""
        minus_locator = (By.ID, f"qty-minus-{product_id}")
        self.click(minus_locator)

    def remove_item(self, product_id: int) -> None:
        """Clicks the remove ('&times;') button on a specific line item."""
        remove_locator = (By.ID, f"cart-remove-{product_id}")
        self.click(remove_locator)

    def proceed_to_checkout(self) -> None:
        """
        Clicks the 'Proceed to Checkout' button inside the cart drawer.
        Falls back to a JavaScript click if the footer is hidden in an empty cart state.
        """
        try:
            self.click(self.CHECKOUT_BTN, timeout=2)
        except Exception:
            btn = self.driver.find_element(*self.CHECKOUT_BTN)
            self.driver.execute_script("arguments[0].click();", btn)

    def is_checkout_modal_open(self) -> bool:
        """Checks if the demo checkout modal is currently displayed."""
        try:
            modal_elem = self.wait_for_element_visible(self.CHECKOUT_MODAL, timeout=2)
            classes = modal_elem.get_attribute("class") or ""
            return "hidden" not in classes.split()
        except Exception:
            return False

    def get_validation_toast_message(self) -> str:
        """Reads the toast message (e.g. for empty cart checkout validation)."""
        return self.get_text(self.TOAST_MESSAGE)
