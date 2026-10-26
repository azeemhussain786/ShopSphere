"""
ShopSphere Automation Test Framework - Pytest Configuration & Fixtures
Centralizes browser lifecycle, server health verification, CLI options,
and professional test failure diagnostics (screenshots, logs, and HTML reports).
"""

import datetime
import logging
import os
import re
import urllib.error
import urllib.request
import pytest
from selenium import webdriver

# ==============================================================================
# Diagnostic Logger Setup
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ShopSphereDiagnostics")


def pytest_addoption(parser):
    """Adds custom command-line options to pytest."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Google Chrome in headless mode for CI/CD environments"
    )


@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for the local ShopSphere application."""
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="session", autouse=True)
def check_flask_server(base_url):
    """
    Session-level pre-flight check.
    Verifies that the Flask web application is actively running and reachable
    before executing any browser tests.
    """
    try:
        with urllib.request.urlopen(base_url, timeout=3) as response:
            if response.status not in (200, 301, 302):
                pytest.fail(
                    f"\n[SERVER ERROR] Flask server returned HTTP status {response.status} at {base_url}."
                )
    except Exception as exc:
        pytest.fail(
            f"\n\n[SERVER NOT RUNNING] Could not connect to {base_url} ({exc}).\n"
            f"The ShopSphere Flask application must be running before executing tests.\n"
            f"Please run the server in a separate terminal using:\n"
            f"    .\\.venv\\Scripts\\python.exe app.py\n"
        )


@pytest.fixture(scope="function")
def driver(request):
    """
    Function-scoped WebDriver fixture.
    Initializes a fresh Chrome browser session for each test case to ensure
    test isolation, and reliably terminates the browser session during teardown.
    Attaches the active driver to the test node for failure diagnostics.
    """
    headless_mode = request.config.getoption("--headless")

    options = webdriver.ChromeOptions()
    if headless_mode:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Selenium 4 uses Selenium Manager automatically to resolve Chrome Driver
    browser = webdriver.Chrome(options=options)
    
    # Store reference on test node so pytest_runtest_makereport can access it on failure
    request.node._driver = browser

    # Yield the active browser instance to the requesting test
    yield browser

    # Teardown: ensure clean browser termination
    browser.quit()


# ==============================================================================
# Failure Diagnostics Hook (Screenshot Capture & HTML Report Integration)
# ==============================================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook executed after each phase of test execution (setup, call, teardown).
    When a failure occurs during the actual test run ('call' phase):
    1. Captures a screenshot from the live browser before teardown occurs.
    2. Saves the image to 'test-results/screenshots/' with a timestamped filename.
    3. Integrates the screenshot and metadata into pytest-html reports.
    4. Emits safe diagnostic logs (URL, Title, Test Name) without exposing secrets.
    """
    outcome = yield
    report = outcome.get_result()

    # Only process failures that occur during the actual test execution ('call' phase)
    if report.when == "call" and report.failed:
        # Retrieve the driver instance associated with this test
        driver = getattr(item, "_driver", None)
        if driver is None and hasattr(item, "funcargs"):
            driver = item.funcargs.get("driver")

        if driver is not None:
            _capture_failure_diagnostics(item, report, driver)


def _capture_failure_diagnostics(item, report, driver):
    """
    Helper function to safely capture failure screenshots and diagnostic metadata.
    Handles all internal exceptions gracefully to prevent masking the original test error.
    """
    try:
        test_name = item.name

        # Extract current page metadata safely
        current_url = "Unavailable"
        page_title = "Unavailable"
        try:
            current_url = driver.current_url
            page_title = driver.title
        except Exception as meta_err:
            logger.warning(f"Could not read page metadata on failure: {meta_err}")

        # Diagnostic log message (safe, no credentials or tokens)
        logger.error(
            f"\n{'='*75}\n"
            f"[TEST FAILURE DETECTED]\n"
            f"Test Case : {item.nodeid}\n"
            f"Page URL  : {current_url}\n"
            f"Page Title: {page_title}\n"
            f"{'='*75}"
        )

        # Prepare screenshot directory: test-results/screenshots/
        project_root = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(project_root, "test-results", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # Generate a safe, descriptive, and unique filename
        sanitized_name = re.sub(r"[^\w\-_\.]", "_", test_name)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"{sanitized_name}_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

        # 1. Save screenshot file to disk
        driver.save_screenshot(screenshot_path)
        logger.info(f"[FAILURE DIAGNOSTIC] Screenshot saved to disk: {screenshot_path}")

        # 2. Attach to pytest-html report if plugin is active
        try:
            import pytest_html

            # Capture as Base64 for fully self-contained HTML report embedding
            base64_data = driver.get_screenshot_as_base64()

            extras = getattr(report, "extras", [])
            if extras is None:
                extras = []

            # Append failure screenshot and safe diagnostic metadata
            extras.append(pytest_html.extras.png(base64_data, name="Failure Screenshot"))
            extras.append(
                pytest_html.extras.html(
                    f'<div style="margin: 8px 0; padding: 10px; background: #fff1f2; '
                    f'border-left: 4px solid #e11d48; border-radius: 4px; font-family: monospace; font-size: 12px;">'
                    f'<strong>Diagnostic Info:</strong><br>'
                    f'<strong>URL:</strong> {current_url}<br>'
                    f'<strong>Title:</strong> {page_title}<br>'
                    f'<strong>Disk Path:</strong> {screenshot_path}'
                    f'</div>'
                )
            )
            report.extras = extras
        except Exception as html_err:
            logger.warning(f"Could not attach screenshot to pytest-html report: {html_err}")

    except Exception as diag_err:
        # Prevent any diagnostic error from obscuring the real test failure
        logger.warning(f"[FAILURE DIAGNOSTIC] Screenshot capture failed: {diag_err}")
