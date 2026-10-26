"""
ShopSphere Page Object Model - Base Page Class
Provides reusable, explicit-wait wrapped methods for browser automation.
Encapsulates Selenium 4 interaction patterns for reliability and readability.
"""

from typing import Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Base class that all Page Objects inherit from.
    Contains common browser automation utilities using explicit waits.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """Explicitly waits until the element is located and visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """Explicitly waits until the element is located and clickable."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """Waits for an element to be clickable and performs a click."""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()

    def type_text(self, locator: Tuple[str, str], text: str, timeout: int = 10) -> None:
        """Waits for an element to be visible, clears existing text, and types new text."""
        element = self.wait_for_element_visible(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str], timeout: int = 10) -> str:
        """Waits for an element to be visible and returns its trimmed inner text."""
        element = self.wait_for_element_visible(locator, timeout)
        return element.text.strip()

    def is_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Checks if an element is visible on the page within the given timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Finds and returns a list of all matching WebElements currently on the DOM."""
        return self.driver.find_elements(*locator)

    def wait_for_text_to_be_present(self, locator: Tuple[str, str], text: str, timeout: int = 10) -> bool:
        """Waits until the specified text is present inside the given element."""
        return WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )

    def get_title(self) -> str:
        """Returns the current document title."""
        return self.driver.title

    def scroll_to_element(self, locator: Tuple[str, str]) -> WebElement:
        """Scrolls the element into view using JavaScript."""
        element = self.wait_for_element_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        return element
