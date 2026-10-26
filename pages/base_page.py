
"""
ShopSphere Page Object Model - Base Page Class.
Reusable Selenium helpers with explicit waits and reliable clicking.
"""

import logging
from typing import Tuple

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    """Common methods inherited by ShopSphere page objects."""

    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, base_url=""):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def load(self, path="/"):
        """Navigate to a page."""
        self.driver.get(f"{self.base_url}/{path.lstrip('/')}")

    def find_element(self, locator: Tuple[str, str]):
        """Find one element."""
        return self.driver.find_element(*locator)

    def find_elements(self, locator: Tuple[str, str]) -> list:
        """Find all matching elements."""
        return self.driver.find_elements(*locator)

    def wait_for_element_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for an element to become visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_visible(self, locator, timeout=DEFAULT_TIMEOUT):
        """Alias for wait_for_element_visible."""
        return self.wait_for_element_visible(locator, timeout)

    def wait_for_clickable(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for an element to become clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_present(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for an element to exist in the DOM."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_elements_present(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait for matching elements to exist."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator, timeout=DEFAULT_TIMEOUT):
        """Scroll to an element and retry transient click failures."""
        for attempt in range(2):
            try:
                element = self.wait_for_present(locator, timeout)

                self.driver.execute_script(
                    """
                    arguments[0].scrollIntoView({
                        behavior: 'instant',
                        block: 'center',
                        inline: 'nearest'
                    });
                    """,
                    element,
                )

                element = self.wait_for_clickable(locator, timeout)
                element.click()
                return

            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
                TimeoutException,
            ):
                logger.warning(
                    "Click attempt %s failed for locator %s",
                    attempt + 1,
                    locator,
                )
                if attempt == 1:
                    raise

    def type_text(
        self, locator, text, clear_first=True, timeout=DEFAULT_TIMEOUT
    ):
        """Type into a visible input field."""
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator, timeout=DEFAULT_TIMEOUT):
        """Get visible text from an element."""
        return self.wait_for_element_visible(locator, timeout).text.strip()

    def get_attribute(self, locator, attribute, timeout=DEFAULT_TIMEOUT):
        """Get an element attribute."""
        return self.wait_for_present(locator, timeout).get_attribute(attribute)

    def is_visible(self, locator):
        """Return whether a matching element is visible."""
        try:
            return any(
                element.is_displayed()
                for element in self.find_elements(locator)
            )
        except StaleElementReferenceException:
            return False

    def is_present(self, locator):
        """Return whether a matching element exists."""
        return len(self.find_elements(locator)) > 0

    def wait_for_url_contains(self, text, timeout=DEFAULT_TIMEOUT):
        """Wait until the URL contains the requested text."""
        return WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )

    def scroll_to_element(self, locator, timeout=DEFAULT_TIMEOUT):
        """Scroll an element into the centre of the viewport."""
        element = self.wait_for_present(locator, timeout)
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center',
                inline: 'nearest'
            });
            """,
            element,
        )
        return element

    def wait_for_element_invisible(self, locator, timeout=DEFAULT_TIMEOUT):
        """Wait until an element is invisible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def refresh(self):
        """Refresh the current page."""
        self.driver.refresh()

    def get_title(self):
        """Return the current page title."""
        return self.driver.title

    def get_current_url(self):
        """Return the current URL."""
        return self.driver.current_url
