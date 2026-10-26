# ShopSphere — Project Documentation

**Project:** ShopSphere — E-commerce Checkout Automation Framework  
**Technology stack:** Python, Flask, HTML, CSS, JavaScript, Selenium WebDriver, Pytest, GitHub Actions  
**Status:** Working demo application with automated UI and API tests  
**Repository:** https://github.com/azeemhussain786/ShopSphere

---

## 1. Project Overview

ShopSphere is a demonstration e-commerce application designed to showcase web development, backend validation, automated testing, and continuous integration.

Users can explore a product catalogue, search and filter products, sort prices, add items to a shopping cart, change quantities, and proceed through a simulated checkout.

The project also contains automated tests that verify the website's behaviour and validate backend API requests.

**Important:** This is a portfolio and testing project. It does not process real payments or represent a production-ready commerce platform.

## 2. Objectives

- Build an interactive e-commerce website.
- Implement a Flask backend and JSON API.
- Validate checkout data on the server.
- Automate browser interactions with Selenium.
- Test API responses and invalid input using Pytest.
- Run tests automatically through GitHub Actions.
- Produce reproducible test results for demonstration and placement interviews.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend and test code |
| Flask | Web application and REST-style endpoints |
| HTML | Page structure |
| CSS | Layout and visual design |
| JavaScript | Search, filtering, cart and checkout interactions |
| Selenium WebDriver | Browser automation |
| Pytest | Automated test execution and assertions |
| Git and GitHub | Version control and source hosting |
| GitHub Actions | Automated CI test workflow |

## 4. Architecture

The project follows a simple client-server structure.

1. **Frontend:** Displays the catalogue and manages interactive elements.
2. **Flask backend:** Serves the website and exposes JSON endpoints.
3. **Checkout API:** Validates submitted cart items and calculates totals using server-side catalogue prices.
4. **Automation layer:** Uses Selenium page objects to interact with the browser.
5. **API test layer:** Uses Flask's test client to test endpoints without opening a browser.
6. **CI pipeline:** Runs automated tests after code is pushed to GitHub.

### Request flow

Browser → Flask application → Checkout validation → Server-calculated total → JSON response → Browser confirmation.

The next development milestone is to connect the frontend's checkout action to this API. Until that integration is completed and tested, the frontend demo checkout and backend API should be considered separate flows.

## 5. Repository Structure

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
│   ├── __init__.py
│   ├── test_homepage.py
│   ├── test_search_and_filter.py
│   ├── test_cart_operations.py
│   └── test_api.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── .github/
    └── workflows/
        └── selenium-tests.yml
```

The documentation is stored in `docs/PROJECT_DOCUMENTATION.md`.

## 6. Backend API

### GET `/api/products`

Returns the product catalogue as JSON.

Expected successful response structure:

```json
{
  "status": "success",
  "count": 18,
  "products": []
}
```

Each product includes fields such as its ID, name, category, price, rating, image URL and description.

### POST `/api/checkout`

Accepts a JSON request containing cart items.

Example request:

```json
{
  "customer_name": "Demo Customer",
  "items": [
    {
      "id": 1,
      "quantity": 2
    }
  ],
  "total_amount": 1
}
```

The supplied total is deliberately untrusted. The backend should calculate the total using the product IDs, quantities and prices stored on the server.

The current automated test verifies that two units of product ID 1, priced at ₹4,999 each, produce a total of ₹9,998 even when the request supplies a fake total.

Invalid carts and quantities are rejected. Order confirmation is simulated; no real payment is made.

## 7. Automated Testing Strategy

### API tests

The API suite checks:

- Successful product catalogue responses.
- Required product fields and unique product IDs.
- Empty or missing cart items.
- Invalid cart structures.
- Unknown product IDs.
- Invalid quantities, including zero, negative values, strings, null and fractional quantities.
- Server-side total calculation rather than trusting a client-supplied total.

### Selenium UI tests

The browser suite checks:

- Homepage content.
- Product search.
- Category filtering.
- Price sorting.
- Adding products to the cart.
- Quantity changes and subtotal calculations.
- Checkout validation when the cart is empty.

### Latest verified local result

**21 automated tests passed:** 14 API tests and 7 Selenium UI tests.

### Latest verified GitHub Actions result

The workflow for commit `f4a3f5c7d24d143f1b686d83cb2c418dad5604cb` completed successfully.

Run details: https://github.com/azeemhussain786/ShopSphere/actions/runs/40308642720

These results describe the tested version at that commit. Rerun the suite after future code changes.

## 8. Local Setup

Open PowerShell in the project directory:

```powershell
cd "$HOME\OneDrive\Desktop\ShopSphere"
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies if necessary:

```powershell
python -m pip install -r requirements.txt
```

Start the Flask server:

```powershell
python app.py
```

Open the application in a browser at:

http://127.0.0.1:5000

Keep the Flask terminal running while executing the current test suite.

## 9. Running Tests

Run API tests:

```powershell
.\.venv\Scripts\pytest.exe tests/test_api.py -v
```

Run the full test suite in headless browser mode:

```powershell
.\.venv\Scripts\pytest.exe tests/ -v --headless
```

Generate an HTML test report:

```powershell
New-Item -ItemType Directory -Force reports
.\.venv\Scripts\pytest.exe tests/ -v --headless --html=reports/test_execution_report.html --self-contained-html
```

The report is generated locally and should not be committed unless the project deliberately chooses to version test reports.

## 10. Continuous Integration

The GitHub Actions workflow is located at:

`.github/workflows/selenium-tests.yml`

It runs when code is pushed to the configured branch or a pull request is opened, according to the workflow triggers.

The workflow prepares Python, installs dependencies, starts the Flask server, waits for readiness, runs the Selenium tests in headless mode, and uploads test diagnostics and reports when configured.

Review workflow status here:

https://github.com/azeemhussain786/ShopSphere/actions

## 11. Current Limitations

- The checkout is a simulation, not a real payment workflow.
- Orders are not persisted to a database.
- Authentication and user accounts are not implemented.
- Inventory is demonstration data.
- The frontend checkout must be connected to the backend checkout API and tested end to end.
- Production deployment would require additional security, logging, configuration, persistence and operational controls.

## 12. Planned Improvements

1. Connect the frontend checkout flow to the Flask checkout API.
2. Add integration tests for the complete checkout flow.
3. Improve error handling and loading feedback in the user interface.
4. Add persistent order storage if the project requirements justify a database.
5. Expand negative and boundary-value tests.
6. Review accessibility, security and maintainability.
7. Document new features and test results after each milestone.

## 13. Placement Interview Explanation

ShopSphere is an e-commerce demonstration application built with Flask and JavaScript, with a focus on automated testing. I implemented browser tests using Selenium and Pytest, API tests for product and checkout validation, and a GitHub Actions workflow to run tests automatically. A key validation rule is that the backend calculates checkout totals from trusted catalogue prices instead of accepting totals supplied by the client. The current project is a simulation and does not process real payments.

---

**Maintenance rule:** Update this document whenever the implementation, test coverage, setup instructions or CI workflow changes. Never report a test as passing unless it has actually been executed successfully.