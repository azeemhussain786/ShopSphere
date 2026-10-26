"""
ShopSphere Automation Test Suite - Search, Category Filtering, and Price Sorting
Tests dynamic catalogue querying, real-time client search, and price ordering.
"""

from pages.home_page import HomePage


def test_search_keyword_filters_catalogue(driver, base_url):
    """
    Test Case: Search Products by Keyword
    1. Loads the homepage catalogue.
    2. Enters 'webcam' into the search input.
    3. Verifies that only products matching 'webcam' remain visible.
    4. Verifies the status count text reflects the filtered count.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Search for 'webcam'
    home_page.search_product("webcam")

    # Verify at least one matching product is found
    visible_count = home_page.get_visible_product_count()
    assert visible_count == 1, (
        f"Expected exactly 1 product matching 'webcam', but found {visible_count}."
    )

    # Verify each visible card contains 'webcam' in the title
    titles = home_page.get_visible_product_titles()
    assert len(titles) == 1, "Expected exactly 1 title in search results."
    assert "webcam" in titles[0].lower(), (
        f"Expected product title to contain 'webcam', but got '{titles[0]}'."
    )

    # Verify status bar count
    count_text = home_page.get_product_count_text()
    assert "1 product" in count_text, (
        f"Expected product status bar to indicate '1 product', but got '{count_text}'."
    )


def test_filter_by_category_smart_home(driver, base_url):
    """
    Test Case: Filter Products by Category Pill
    1. Loads the homepage catalogue.
    2. Clicks the 'Smart Home' category pill.
    3. Verifies that exactly 3 Smart Home products are displayed.
    4. Verifies the product status bar displays 'Showing 3 products in "Smart Home"'.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Apply 'Smart Home' filter
    home_page.filter_by_category("Smart Home")

    # Verify count matches the 3 Smart Home items configured in app.py
    visible_count = home_page.get_visible_product_count()
    assert visible_count == 3, (
        f"Expected 3 products in 'Smart Home' category, but found {visible_count}."
    )

    # Verify titles match known Smart Home catalogue items
    titles = home_page.get_visible_product_titles()
    expected_keywords = ["light bar", "air purifier", "smartplug"]
    for expected in expected_keywords:
        assert any(expected in title.lower() for title in titles), (
            f"Expected a product containing '{expected}' in Smart Home category titles: {titles}."
        )

    # Verify status bar text
    count_text = home_page.get_product_count_text()
    assert "3 products" in count_text, (
        f"Expected status bar to mention '3 products', but got '{count_text}'."
    )
    assert "Smart Home" in count_text, (
        f"Expected status bar to mention 'Smart Home', but got '{count_text}'."
    )


def test_sort_products_by_price_low_to_high(driver, base_url):
    """
    Test Case: Sort Catalogue Products by Price (Low to High)
    1. Loads the homepage catalogue.
    2. Selects 'Price: Low to High' from the sort dropdown.
    3. Extracts numeric prices from all visible cards.
    4. Verifies that prices are sorted in strict ascending numerical order.
    """
    home_page = HomePage(driver, base_url)
    home_page.load()

    # Trigger price sort: low to high
    home_page.sort_by("price-low")

    # Extract all visible prices as floats
    prices = home_page.get_visible_product_prices()

    assert len(prices) == 18, (
        f"Expected all 18 products to remain visible after sorting, found {len(prices)}."
    )

    # Verify numeric sorting
    expected_sorted_prices = sorted(prices)
    assert prices == expected_sorted_prices, (
        f"Prices are not in ascending order!\nActual: {prices}\nExpected: {expected_sorted_prices}"
    )

    # Double-check first (lowest) and last (highest) prices
    assert prices[0] <= prices[-1], (
        f"Lowest price ({prices[0]}) should be less than or equal to highest price ({prices[-1]})."
    )
