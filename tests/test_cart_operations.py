"""
ShopSphere Automation Test Suite - Shopping Cart & Checkout Validation
Tests adding items, badge incrementing, quantity adjustments, subtotal math, and empty-cart guards.
"""

from pages.home_page import HomePage
from pages.cart_drawer import CartDrawer


def test_add_to_cart_increments_badge_and_shows_toast(driver, base_url):
    """
    Test Case: Add Product to Cart
    1. Loads homepage with a fresh in-memory cart (badge = 0).
    2. Clicks 'Add to Cart' on product ID 1 (Aura Pro Wireless ANC Headphones).
    3. Verifies that the top navigation cart badge increments immediately to 1.
    4. Verifies that the confirmation toast appears with the correct product name.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Initial state verification
    assert home_page.get_cart_badge_count() == 0, "Cart badge should initially be 0."

    # Add Product ID 1 (Aura Pro Wireless ANC Headphones)
    home_page.add_product_to_cart_by_id(1)

    # Verify navbar badge increments to 1
    badge_count = home_page.get_cart_badge_count()
    assert badge_count == 1, (
        f"Expected cart badge to be 1 after adding 1 item, but got {badge_count}."
    )

    # Verify toast notification message
    toast_text = home_page.get_toast_message()
    assert "Aura Pro Wireless ANC Headphones" in toast_text, (
        f"Expected toast to mention 'Aura Pro Wireless ANC Headphones', but got '{toast_text}'."
    )


def test_cart_drawer_quantity_increase_and_subtotal(driver, base_url):
    """
    Test Case: Increase Item Quantity & Validate Recalculated Subtotals
    1. Loads homepage and adds Product ID 1 (Aura Pro Wireless ANC Headphones @ ₹4,999).
    2. Opens the cart drawer and confirms it is open.
    3. Verifies initial quantity is 1, line subtotal is ₹4,999.0, and cart total is ₹4,999.0.
    4. Clicks '+' to increase quantity to 2.
    5. Verifies quantity updates to 2.
    6. Verifies line item subtotal and cart total recalculate to ₹9,998.0 (2 * ₹4,999).
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Add Product 1 (@ ₹4,999)
    home_page.add_product_to_cart_by_id(1)

    # Open cart drawer
    home_page.open_cart_drawer()
    cart_drawer = CartDrawer(driver)
    assert cart_drawer.is_drawer_open(), "Cart drawer should be open."

    # Verify initial quantity & price
    assert cart_drawer.get_item_quantity(1) == 1, "Initial item quantity should be 1."
    assert cart_drawer.get_subtotal_amount() == 4999.0, "Initial subtotal should be ₹4,999."
    assert cart_drawer.get_total_amount() == 4999.0, "Initial total should be ₹4,999."

    # Increase quantity to 2
    cart_drawer.increase_quantity(1)

    # Verify updated quantity
    updated_qty = cart_drawer.get_item_quantity(1)
    assert updated_qty == 2, (
        f"Expected quantity to be 2 after clicking '+', but got {updated_qty}."
    )

    # Verify recalculated subtotals (2 * 4999 = 9998)
    expected_subtotal = 4999.0 * 2
    item_subtotal = cart_drawer.get_item_subtotal(1)
    cart_subtotal = cart_drawer.get_subtotal_amount()
    cart_total = cart_drawer.get_total_amount()

    assert item_subtotal == expected_subtotal, (
        f"Expected line subtotal to be ₹{expected_subtotal}, got ₹{item_subtotal}."
    )
    assert cart_subtotal == expected_subtotal, (
        f"Expected cart subtotal to be ₹{expected_subtotal}, got ₹{cart_subtotal}."
    )
    assert cart_total == expected_subtotal, (
        f"Expected cart total to be ₹{expected_subtotal}, got ₹{cart_total}."
    )


def test_empty_cart_checkout_validation(driver, base_url):
    """
    Test Case: Empty Cart Checkout Guard & Validation
    1. Loads homepage with a fresh, empty cart.
    2. Opens the cart drawer.
    3. Verifies the empty cart illustration/state is visible.
    4. Triggers checkout on the empty cart.
    5. Verifies that checkout is blocked, validation toast is displayed,
       and the checkout modal is NOT opened.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Open cart drawer without adding any items
    home_page.open_cart_drawer()
    cart_drawer = CartDrawer(driver)
    assert cart_drawer.is_drawer_open(), "Cart drawer should be open."

    # Verify empty state is rendered
    assert cart_drawer.is_empty_state_visible(), (
        "Empty cart state message should be displayed when cart contains no items."
    )

    # Trigger checkout action
    cart_drawer.proceed_to_checkout()

    # Verify empty cart warning toast appears
    toast_msg = cart_drawer.get_validation_toast_message()
    assert "empty" in toast_msg.lower(), (
        f"Expected validation toast to indicate cart is empty, but got '{toast_msg}'."
    )

    # Verify checkout modal was NOT opened
    assert not cart_drawer.is_checkout_modal_open(), (
        "Checkout modal should not open when attempting to checkout with an empty cart."
    )
