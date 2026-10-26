# ShopSphere — E-commerce Checkout Automation Framework

An e-commerce demo application with automated UI, API, and checkout regression testing using Python, Selenium, Flask, and Pytest.

## Project Overview

ShopSphere demonstrates how an e-commerce application can be tested using a structured automation framework. It combines browser-based testing with API validation and continuous integration through GitHub Actions.

**This is a demonstration project. Checkout simulates order placement and does not process real payments.**

## Features

- Product catalogue with category filtering and search
- Product sorting by price
- Shopping cart with quantity updates and subtotal calculations
- Checkout form validation
- Flask REST API for product data and checkout validation
- Server-side product price calculation
- Selenium browser automation
- Pytest API and UI regression tests
- Automated CI workflow using GitHub Actions
- Test reports and failure diagnostics

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and test code |
| Flask | Web application and REST API |
| Selenium | Browser automation |
| Pytest | Test execution and assertions |
| pytest-html | HTML test reports |
| HTML, CSS, JavaScript | Frontend |
| Git and GitHub | Version control |
| GitHub Actions | Continuous integration |

## Architecture

1. **Frontend:** Users browse products, manage the cart, and enter checkout details.
2. **Flask application:** Serves the website and exposes product and checkout endpoints.
3. **API validation:** Validates checkout items and quantities against the product catalogue.
4. **Automation framework:** Selenium tests browser interactions; API tests validate backend behavior.
5. **Continuous integration:** GitHub Actions runs the automated test suite on pushes and pull requests targeting `main`.

## API Endpoints

### `GET /api/products`

Returns the product catalogue in JSON format.

### `POST /api/checkout`

Accepts customer information and cart items, validates the request, and calculates the order total using server-side catalogue prices.

Example request body:

```json
{
  "customer_name": "Rahul Sharma",
  "items": [
    {
      "id": 1,
      "quantity": 2
    }
  ]
}
```

The actual product ID and total depend on the current catalogue. The API is for demonstration purposes only.

## Project Structure

```text
ShopSphere/
├── app.py
├── conftest.py
├── requirements.txt
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── home_page.py
│   └── cart_drawer.py
├── tests/
│   ├── test_api.py
│   ├── test_homepage.py
│   ├── test_search_and_filter.py
│   └── test_cart_operations.py
├── templates/
├── static/
│   ├── css/
│   └── js/
├── docs/
│   └── PROJECT_DOCUMENTATION.md
└── .github/
    └── workflows/
        └── selenium-tests.yml
```

## Setup Instructions

Prerequisites: Python 3.13, Git, and a compatible Chrome browser.

Clone the repository:

```bash
git clone https://github.com/azeemhussain786/ShopSphere.git
cd ShopSphere
```

Create and activate a virtual environment on Windows:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Run Automated Tests

Keep the Flask application running in one terminal. In a second terminal, activate the virtual environment and run:

```powershell
pytest tests/ -v
```

Run Selenium tests in headless mode:

```powershell
pytest tests/ -v --headless
```

Generate an HTML report:

```powershell
New-Item -ItemType Directory -Force reports
pytest tests/ -v --html=reports/test_execution_report.html --self-contained-html
```

The report is generated locally and should not be committed unless the project is intentionally configured to version reports.

## Continuous Integration

The GitHub Actions workflow is located at `.github/workflows/selenium-tests.yml`.

It runs automated tests in a CI environment and can upload test reports and diagnostic artifacts. View the [workflow runs](https://github.com/azeemhussain786/ShopSphere/actions).

## Limitations

- Checkout is simulated; no real payment gateway is integrated.
- Product data is demonstration data.
- This project is an automation and testing demonstration, not a production-ready commerce platform.

## Future Improvements

- Add test coverage for invalid and interrupted checkout flows.
- Add accessibility and responsive-layout tests.
- Improve test reporting and failure screenshots.
- Add API schema validation and security-focused test cases.
- Introduce a database and persistent order storage if the application is expanded.

## Author

**Azeem Hussain**

Project repository: https://github.com/azeemhussain786/ShopSphere
