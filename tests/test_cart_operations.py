
"""
ShopSphere Automation Test Suite - Shopping Cart & Checkout
Covers cart operations, empty-cart validation, and API-backed checkout.
"""

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage
from pages.cart_drawer import CartDrawer


def test_add_to_cart_increments_badge_and_shows_toast(driver, base_url):
    """Adding a product updates the cart badge and confirmation toast."""
    home_page = HomePage(driver, base_url)
    home_page.load()

    assert home_page.get_cart_badge_count() == 0

    home_page.add_product_to_cart_by_id(1)

    assert home_page.get_cart_badge_count() == 1
    assert "Aura Pro Wireless ANC Headphones" in home_page.get_toast_message()


def test_cart_drawer_quantity_increase_and_subtotal(driver, base_url):
    """Increasing quantity updates the line subtotal and cart total."""
    home_page = HomePage(driver, base_url)
    home_page.load()
    home_page.add_product_to_cart_by_id(1)
    home_page.open_cart_drawer()

    cart_drawer = CartDrawer(driver)
    assert cart_drawer.is_drawer_open()
    assert cart_drawer.get_item_quantity(1) == 1
    assert cart_drawer.get_subtotal_amount() == 4999.0
    assert cart_drawer.get_total_amount() == 4999.0

    cart_drawer.increase_quantity(1)

    assert cart_drawer.get_item_quantity(1) == 2
    assert cart_drawer.get_item_subtotal(1) == 9998.0
    assert cart_drawer.get_subtotal_amount() == 9998.0
    assert cart_drawer.get_total_amount() == 9998.0


def test_empty_cart_checkout_validation(driver, base_url):
    """Checkout is blocked when the cart is empty."""
    home_page = HomePage(driver, base_url)
    home_page.load()
    home_page.open_cart_drawer()

    cart_drawer = CartDrawer(driver)
    assert cart_drawer.is_drawer_open()
    assert cart_drawer.is_empty_state_visible()

    cart_drawer.proceed_to_checkout()

    assert "empty" in cart_drawer.get_validation_toast_message().lower()
    assert not cart_drawer.is_checkout_modal_open()


def test_successful_checkout_uses_flask_api(driver, base_url):
    """
    Verify a browser checkout submits an order to Flask and displays
    the server-generated order ID and server-calculated total.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()
    home_page.add_product_to_cart_by_id(1)
    home_page.open_cart_drawer()

    cart_drawer = CartDrawer(driver)
    assert cart_drawer.is_drawer_open()
    cart_drawer.proceed_to_checkout()

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.visibility_of_element_located((By.ID, "checkout-modal"))
    )

    wait.until(
        EC.element_to_be_clickable((By.ID, "place-order-btn"))
    ).click()

    def success_view_is_visible(browser):
        element = browser.find_element(By.ID, "checkout-success-view")
        classes = (element.get_attribute("class") or "").split()
        if element.is_displayed() and "hidden" not in classes:
            return element
        return False

    success_view = wait.until(success_view_is_visible)
    assert success_view.is_displayed()

    order_id = wait.until(
        EC.visibility_of_element_located((By.ID, "confirmed-order-id"))
    ).text.strip()

    assert re.fullmatch(r"SP-\d{5}", order_id), (
        f"Expected an order ID like SP-12345, got {order_id!r}"
    )

    customer_name = driver.find_element(
        By.ID, "confirmed-customer-name"
    ).text.strip()
    assert customer_name == "Rahul Sharma"

    confirmed_total = driver.find_element(
        By.ID, "confirmed-order-total"
    ).text.strip()
    assert confirmed_total == "₹4,999", (
        f"Expected server-confirmed total ₹4,999, got {confirmed_total!r}"
    )

    payment_method = driver.find_element(
        By.ID, "confirmed-payment-method"
    ).text.strip()
    assert "Cash on Delivery" in payment_method

    wait.until(
        lambda browser: browser.find_element(
            By.ID, "cart-count"
        ).text.strip() == "0"
    )
    assert home_page.get_cart_badge_count() == 0
