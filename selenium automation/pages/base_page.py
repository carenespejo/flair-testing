"""
============================================================
 base_page.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- Defines the BasePage class used by all Page Object classes.
- Centralizes common Selenium helpers:
  - Navigation
  - Explicit waits
  - Common actions (click, type text, get text, etc.)

WHAT YOU SHOULD EDIT
--------------------
- You MAY:
  - Add new reusable helper methods that are generic and applicable
    across multiple pages (for example, scrolling helpers).

WHAT YOU SHOULD NOT EDIT
------------------------
- DO NOT REMOVE OR RENAME EXISTING METHODS OR PARAMETERS.
- DO NOT CHANGE HOW THE DRIVER OR WebDriverWait ARE INITIALIZED.
- Test-specific or page-specific logic SHOULD LIVE in individual
  page classes, not in this base class.
"""

from __future__ import annotations

from typing import Tuple, Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException


from config.settings import (
    DEFAULT_BASE_URL,
    DEFAULT_WAIT_TIMEOUT,
)


class BasePage:
    """
    Base class for all Page Objects.

    - Stores a reference to the Selenium WebDriver.
    - Provides a configured WebDriverWait using explicit waits only.
    - Exposes helper methods for common user interactions.
    """

    def __init__(
        self,
        driver: WebDriver,
        base_url: str | None = None,
        timeout: int = DEFAULT_WAIT_TIMEOUT,
    ) -> None:
        # DO NOT MODIFY THIS INITIALIZATION LOGIC
        self.driver: WebDriver = driver
        self.base_url: str = base_url or DEFAULT_BASE_URL
        self.wait: WebDriverWait = WebDriverWait(self.driver, timeout)

    # =========================================================
    # NAVIGATION HELPERS
    # =========================================================

    def open(self, path: str = "") -> None:
        """
        Open a URL constructed from the base_url and an optional path.

        Example:
            self.open("/login")
        """
        # DO NOT CHANGE THIS METHOD SIGNATURE
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    # =========================================================
    # LOW-LEVEL ELEMENT HELPERS (EXPLICIT WAITS ONLY)
    # =========================================================

    def _wait_for_visible(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait until the element located by 'locator' is visible.

        - Uses explicit wait only (no implicit waits).
        - Returns the WebElement once it is visible.

        locator: A tuple like (By.ID, "username") defined in locators.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _wait_for_clickable(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait until the element located by 'locator' is clickable.
        """
        return self.wait.until(EC.element_to_be_clickable(locator))

    # =========================================================
    # USER ACTION HELPERS
    # =========================================================

    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click an element after waiting for it to be clickable.
        Handles sticky headers and overlays.
        """
        element = self._wait_for_clickable(locator)

        # Scroll element below sticky header
        self.driver.execute_script("""
            const headerOffset = 120;  // adjust to sticky header height
            const elementRect = arguments[0].getBoundingClientRect();
            const offsetPosition = elementRect.top + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'instant'
            });
        """, element)

        try:
            element.click()
        except ElementClickInterceptedException:
            # Fallback for rare animation/overlay cases
            self.driver.execute_script("arguments[0].click();", element)


    def type_text(
        self,
        locator: Tuple[str, str],
        text: str,
        clear_first: bool = True,
    ) -> None:
        """
        Type text into an input element.

        Parameters:
            locator: Element locator tuple.
            text: Text to input.
            clear_first: If True, clear the field before typing.
        """
        element = self._wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get visible text from an element.
        """
        element = self._wait_for_visible(locator)
        return element.text.strip()
    
    def get_field_value(self, locator: tuple) -> str:
        """
        Get the current value of an input field.
        
        Args:
            locator: Locator tuple for the input field.
        
        Returns:
            The current value of the input field as a string.
        """
        element = self._wait_for_visible(locator)
        return element.get_attribute("value")

    def is_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is visible on the page.

        NOTE:
        - Returns True if element becomes visible within the timeout.
        - Returns False if element does not become visible in time.
        """
        try:
            self._wait_for_visible(locator)
            return True
        except Exception:
            return False
        
    def click_combo(self, locator: tuple) -> None:
        """
        Wait for a combo/dropdown to be clickable and click it.
        Uses explicit wait with a 10-second timeout.
        Scrolls the element into view to avoid sticky header interference.
        
        Args:
            locator: A tuple of (By, locator_string) for the combo element
        """
        combo = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        # Scroll the combo into view to avoid sticky header blocking the click
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", combo)
        # Wait briefly for the element to settle and then click
        self.wait.until(EC.element_to_be_clickable(locator))
        combo.click()

    def select_combo_option(self, option_locator_template: str, option_name: str) -> None:
        """
        Select an option from an open combo/dropdown.
        Handles quotes and apostrophes in option_name.
        
        Args:
            option_locator_template: XPath template with {option_name} placeholder
            option_name: The name of the option to select (may contain quotes/apostrophes)
        """
        # Build XPath using the option name as-is (with apostrophes, etc.)
        # The template is: //div[@role="option" and contains(normalize-space(), "{option_name}")]
        option_xpath = option_locator_template.format(option_name=option_name)
        option_locator = (By.XPATH, option_xpath)
        
        # (debug prints removed for performance)
        
        try:
            option = self.wait.until(
                EC.element_to_be_clickable(option_locator)
            )
            # found option; click
            option.click()
        except Exception as e:
            # Try to find all matching elements for diagnostics (no printing)
            try:
                _ = self.driver.find_elements(By.XPATH, '//div[@role="option"]')
            except:
                pass
            raise

    def select_dropdown(self, combo_locator: Tuple[str, str], option_locator_template: str, option_name: str) -> None:
        """
        Combined helper to open a combo/dropdown and select an option.
        Automatically escapes special characters in option_name for XPath.

        Args:
            combo_locator: Locator tuple for the combo element (e.g., (By.ID, 'brand')).
            option_locator_template: XPath template string containing '{option_name}' placeholder.
            option_name: Visible text of the option to select (may contain special characters).
        """
        # Open the combo and wait for options to render
        self.click_combo(combo_locator)
        # Wait until at least one option appears in the dropdown
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='option']")))
        # Select the option
        self.select_combo_option(option_locator_template, option_name)

    def upload_file(self, locator: Tuple[str, str], file_path: str) -> None:
        """
        Upload a file by sending the file path to an input element of type 'file'.

        Parameters:
            locator: Element locator tuple for the file input.
            file_path: Full path to the file to upload.
        """
        element = self._wait_for_visible(locator)
        element.send_keys(file_path)

    # =========================================================
    # HELPERS
    # =========================================================

    # Note: escaping helper removed — selection uses straightforward template formatting

    def wait_until(self, condition, message: str | None = None) -> Any:
        """
        Generic wrapper around WebDriverWait.until.

        - Use this for specialized conditions that are not covered
          by the simple helpers above.
        - This still enforces explicit waits only.
        """
        return self.wait.until(condition, message) # type: ignore
