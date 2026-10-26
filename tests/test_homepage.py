"""
ShopSphere Automation Test Suite - Homepage Verification
Tests homepage loading, exact page title, and presence of core branding/hero content.
"""

from pages.home_page import HomePage


def test_homepage_title_and_content(driver, base_url):
    """
    Test Case: Verify ShopSphere Homepage Loading & Core UI Content
    1. Opens the application via the HomePage object.
    2. Verifies the page title matches 'ShopSphere - Modern E-Commerce'.
    3. Verifies that the brand logo and hero banner title are clearly visible.
    4. Verifies that product cards are loaded on the catalogue grid.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Verify exact document title
    actual_title = home_page.get_title()
    assert actual_title != "", "Page title should not be empty."
    assert actual_title == "ShopSphere - Modern E-Commerce", (
        f"Expected title 'ShopSphere - Modern E-Commerce', but got '{actual_title}'."
    )

    # Verify brand logo text
    brand_text = home_page.get_brand_logo_text()
    assert "ShopSphere" in brand_text, (
        f"Expected brand logo to contain 'ShopSphere', but got '{brand_text}'."
    )

    # Verify hero section title
    hero_title = home_page.get_hero_title_text()
    assert "Elevate Your Everyday Tech" in hero_title, (
        f"Expected hero title to contain 'Elevate Your Everyday Tech', but got '{hero_title}'."
    )

    # Verify product cards are displayed
    product_count = home_page.get_visible_product_count()
    assert product_count > 0, "Expected at least one product card to be displayed on the homepage."
