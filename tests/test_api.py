
"""
ShopSphere API Automation Tests
Tests the product catalogue and checkout validation.
"""

import pytest

from app import app, PRODUCTS


@pytest.fixture
def api_client():
    """Create an isolated Flask test client for API tests."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_products_api_returns_success(api_client):
    response = api_client.get("/api/products")

    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] == len(PRODUCTS)
    assert isinstance(data["products"], list)


def test_products_api_returns_all_expected_fields(api_client):
    response = api_client.get("/api/products")
    data = response.get_json()

    required_fields = {
        "id",
        "name",
        "category",
        "price",
        "original_price",
        "rating",
        "reviews_count",
        "badge",
        "image_url",
        "description",
    }

    for product in data["products"]:
        assert required_fields.issubset(product.keys())


def test_products_api_has_unique_product_ids(api_client):
    response = api_client.get("/api/products")
    products = response.get_json()["products"]

    product_ids = [product["id"] for product in products]

    assert len(product_ids) == len(set(product_ids))
    assert len(product_ids) == 18


def test_checkout_rejects_empty_cart(api_client):
    response = api_client.post(
        "/api/checkout",
        json={"items": []},
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_checkout_rejects_missing_items(api_client):
    response = api_client.post(
        "/api/checkout",
        json={"customer_name": "Azeem"},
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_checkout_rejects_non_list_items(api_client):
    response = api_client.post(
        "/api/checkout",
        json={"items": "not-a-cart"},
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_checkout_rejects_unknown_product(api_client):
    response = api_client.post(
        "/api/checkout",
        json={
            "items": [
                {"id": 99999, "quantity": 1}
            ]
        },
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


@pytest.mark.parametrize("quantity", [0, -1, "two", None, 1.5])
def test_checkout_rejects_invalid_quantity(api_client, quantity):
    response = api_client.post(
        "/api/checkout",
        json={
            "items": [
                {"id": 1, "quantity": quantity}
            ]
        },
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_checkout_calculates_total_from_catalogue(api_client):
    response = api_client.post(
        "/api/checkout",
        json={
            "customer_name": "Azeem",
            "items": [
                {"id": 1, "quantity": 2}
            ],
            # Deliberately fake total: the server must ignore it.
            "total_amount": 1,
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert data["customer_name"] == "Azeem"
    assert data["total_amount"] == 9998
    assert data["order_id"].startswith("SP-")


def test_checkout_rejects_malformed_cart_item(api_client):
    response = api_client.post(
        "/api/checkout",
        json={
            "items": [
                {"quantity": 1}
            ]
        },
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"
