"""
ShopSphere - E-Commerce Web Application
Flask backend serving the product catalogue, categories, homepage, and demo checkout.
Designed for manual exploration and automated Selenium testing.
"""

import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Expanded Demo Product Catalogue (Prices in INR ₹)
# Categorized across the 6 required domains for portfolio testing
PRODUCTS = [
    # Category 1: Gadgets and Technology
    {
        "id": 1,
        "name": "Aura Pro Wireless ANC Headphones",
        "category": "Gadgets and Technology",
        "price": 4999,
        "original_price": 7999,
        "rating": 4.8,
        "reviews_count": 142,
        "badge": "Best Seller",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
        "description": "Active noise cancelling with 40-hour battery life and spatial audio."
    },
    {
        "id": 2,
        "name": "Vortex 75% Mechanical Keyboard",
        "category": "Gadgets and Technology",
        "price": 3499,
        "original_price": 4999,
        "rating": 4.9,
        "reviews_count": 215,
        "badge": "Top Rated",
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&q=80",
        "description": "RGB backlighting, tactile switches, hot-swappable PCB, and aluminum frame."
    },
    {
        "id": 3,
        "name": "NovaStream 4K Ultra HD Webcam",
        "category": "Gadgets and Technology",
        "price": 2899,
        "original_price": 3999,
        "rating": 4.6,
        "reviews_count": 89,
        "badge": "Trending",
        "image_url": "https://images.unsplash.com/photo-1588508065123-287b28e013da?w=500&q=80",
        "description": "Crisp 4K video calling with dual stereo noise-reducing microphones."
    },

    # Category 2: Mobile Accessories
    {
        "id": 4,
        "name": "Titanium 65W GaN Fast Charger",
        "category": "Mobile Accessories",
        "price": 1899,
        "original_price": 2499,
        "rating": 4.9,
        "reviews_count": 340,
        "badge": "Popular",
        "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500&q=80",
        "description": "Ultra-compact dual USB-C and USB-A fast charging for phones and laptops."
    },
    {
        "id": 5,
        "name": "MagPulse 10000mAh Magnetic Power Bank",
        "category": "Mobile Accessories",
        "price": 2199,
        "original_price": 3299,
        "rating": 4.7,
        "reviews_count": 165,
        "badge": "New",
        "image_url": "https://images.unsplash.com/photo-1609592424360-1e247c433306?w=500&q=80",
        "description": "15W wireless magnetic attachment with 20W Power Delivery wired output."
    },
    {
        "id": 6,
        "name": "Braided Armor 240W USB-C Cable (2m)",
        "category": "Mobile Accessories",
        "price": 599,
        "original_price": 999,
        "rating": 4.8,
        "reviews_count": 420,
        "badge": "Essential",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&q=80",
        "description": "Reinforced double-braided nylon with 480Mbps transfer and 240W PD support."
    },

    # Category 3: Smart Home
    {
        "id": 7,
        "name": "Lumina Smart RGB Ambient Light Bar",
        "category": "Smart Home",
        "price": 2299,
        "original_price": 3499,
        "rating": 4.7,
        "reviews_count": 110,
        "badge": "Trending",
        "image_url": "https://images.unsplash.com/photo-1550009158-9ebf69173e03?w=500&q=80",
        "description": "16 million colors with music sync and voice control via Google Assistant."
    },
    {
        "id": 8,
        "name": "AeroBreeze Smart Air Purifier Mini",
        "category": "Smart Home",
        "price": 4499,
        "original_price": 6999,
        "rating": 4.8,
        "reviews_count": 78,
        "badge": "Eco Choice",
        "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500&q=80",
        "description": "True HEPA H13 filtration removes 99.97% of airborne dust and allergens."
    },
    {
        "id": 9,
        "name": "SmartPlug Pro with Energy Monitor",
        "category": "Smart Home",
        "price": 999,
        "original_price": 1599,
        "rating": 4.5,
        "reviews_count": 195,
        "badge": "Value Pick",
        "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=500&q=80",
        "description": "Control appliances remotely, set schedules, and track live power consumption."
    },

    # Category 4: Lifestyle
    {
        "id": 10,
        "name": "UrbanVoyage Water-Resistant Laptop Backpack",
        "category": "Lifestyle",
        "price": 1799,
        "original_price": 2999,
        "rating": 4.8,
        "reviews_count": 280,
        "badge": "Best Seller",
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&q=80",
        "description": "Dedicated 15.6-inch laptop compartment, ergonomic straps, and USB charging port."
    },
    {
        "id": 11,
        "name": "ThermoShield Insulated Flask 750ml",
        "category": "Lifestyle",
        "price": 849,
        "original_price": 1299,
        "rating": 4.9,
        "reviews_count": 310,
        "badge": "Eco Choice",
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&q=80",
        "description": "Double-wall vacuum insulation keeps liquids cold for 24 hours or hot for 12 hours."
    },
    {
        "id": 12,
        "name": "DeskCraft Dual-Sided Desk Mat",
        "category": "Lifestyle",
        "price": 699,
        "original_price": 1199,
        "rating": 4.6,
        "reviews_count": 145,
        "badge": "Essential",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80",
        "description": "Premium waterproof vegan leather with dual colors and smooth mouse glide."
    },

    # Category 5: Beauty and Personal Care
    {
        "id": 13,
        "name": "SilkGlow Sonic Facial Cleansing Brush",
        "category": "Beauty and Personal Care",
        "price": 1299,
        "original_price": 1999,
        "rating": 4.7,
        "reviews_count": 124,
        "badge": "Top Rated",
        "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=500&q=80",
        "description": "Ultra-hygienic soft silicone bristles with 5 sonic vibration massage modes."
    },
    {
        "id": 14,
        "name": "HydroMist Nano Facial Steamer",
        "category": "Beauty and Personal Care",
        "price": 1499,
        "original_price": 2299,
        "rating": 4.6,
        "reviews_count": 92,
        "badge": "New",
        "image_url": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=500&q=80",
        "description": "Generates warm nano-ionic mist for deep pore cleansing and skin hydration."
    },
    {
        "id": 15,
        "name": "IonicCare Salon Pro Hair Dryer",
        "category": "Beauty and Personal Care",
        "price": 2499,
        "original_price": 3799,
        "rating": 4.8,
        "reviews_count": 188,
        "badge": "Sale",
        "image_url": "https://images.unsplash.com/photo-1522337094846-8a818192de1f?w=500&q=80",
        "description": "1800W motor with negative ion technology to reduce frizz and lock in shine."
    },

    # Category 6: Fitness and Wellness
    {
        "id": 16,
        "name": "PulseTrack Active Fitness Smartwatch",
        "category": "Fitness and Wellness",
        "price": 2799,
        "original_price": 4499,
        "rating": 4.6,
        "reviews_count": 230,
        "badge": "Trending",
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",
        "description": "All-day heart rate, SpO2 tracker, sleep analysis, and 120 sports modes."
    },
    {
        "id": 17,
        "name": "DeepRelief Percussion Massage Gun",
        "category": "Fitness and Wellness",
        "price": 3199,
        "original_price": 5499,
        "rating": 4.9,
        "reviews_count": 175,
        "badge": "Popular",
        "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=500&q=80",
        "description": "High-torque brushless motor with 6 intensity levels and 4 massage heads."
    },
    {
        "id": 18,
        "name": "ProGrip High-Density Non-Slip Yoga Mat",
        "category": "Fitness and Wellness",
        "price": 1099,
        "original_price": 1699,
        "rating": 4.8,
        "reviews_count": 315,
        "badge": "Best Seller",
        "image_url": "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=500&q=80",
        "description": "6mm extra-thick eco-friendly TPE foam with laser-engraved alignment lines."
    }
]

# The 6 canonical categories
CATEGORIES = [
    "Gadgets and Technology",
    "Mobile Accessories",
    "Smart Home",
    "Lifestyle",
    "Beauty and Personal Care",
    "Fitness and Wellness"
]


@app.route("/")
def index():
    """
    Renders the ShopSphere homepage.
    Passes products and categories to templates/index.html.
    """
    return render_template("index.html", products=PRODUCTS, categories=CATEGORIES)


@app.route("/api/products")
def api_products():
    """
    API endpoint returning the product catalogue in JSON format.
    Useful for API verifications and automated tests.
    """
    return jsonify({
        "status": "success",
        "count": len(PRODUCTS),
        "products": PRODUCTS
    })


@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    """
    Validate cart contents against the server-side product catalogue.
    Calculate prices on the server; never trust client-submitted totals.
    This is a simulated checkout and does not process real payments.
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "Request body must be a valid JSON object."
        }), 400

    items = data.get("items")

    if not isinstance(items, list) or not items:
        return jsonify({
            "status": "error",
            "message": "Cart must contain at least one valid item."
        }), 400

    products_by_id = {product["id"]: product for product in PRODUCTS}
    total_amount = 0

    for item in items:
        if not isinstance(item, dict):
            return jsonify({
                "status": "error",
                "message": "Each cart item must be a JSON object."
            }), 400

        product_id = item.get("id")
        quantity = item.get("quantity")

        if isinstance(product_id, bool) or not isinstance(product_id, int):
            return jsonify({
                "status": "error",
                "message": "Each cart item must have an integer product ID."
            }), 400

        if product_id not in products_by_id:
            return jsonify({
                "status": "error",
                "message": f"Product ID {product_id} does not exist."
            }), 400

        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            return jsonify({
                "status": "error",
                "message": "Quantity must be a positive whole number."
            }), 400

        product = products_by_id[product_id]
        total_amount += product["price"] * quantity

    customer_name = data.get("customer_name", "Valued Customer")

    if not isinstance(customer_name, str) or not customer_name.strip():
        customer_name = "Valued Customer"

    order_id = f"SP-{random.randint(10000, 99999)}"

    return jsonify({
        "status": "success",
        "order_id": order_id,
        "message": f"Demo order {order_id} placed successfully!",
        "customer_name": customer_name.strip(),
        "total_amount": total_amount,
        "note": "Portfolio Demo: No real financial transaction occurred."
    })


if __name__ == "__main__":
    # Runs the Flask application on port 5000 in debug mode
    print("Starting ShopSphere server at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
