"""
============================================================
 page_template.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- TEMPLATE for creating new Page Object classes.
- Each page class:
  - Inherits from BasePage.
  - Uses locators from the `locators` package.
  - Provides readable methods that model user actions and queries.

WHAT YOU SHOULD EDIT
--------------------
- RENAME the class and file to match the page it represents.
- UPDATE imports to reference your own locator classes.
- ADD or REMOVE methods to represent real user actions on that page.

WHAT YOU SHOULD NOT EDIT
------------------------
- DO NOT place test assertions in page classes.
  - Assertions belong in test files only.
- DO NOT import PyTest or test modules here.
"""

from __future__ import annotations

from pages.base_page import BasePage
from locators.locators_template import ExampleFormLocators


class ExampleFormPage(BasePage):
    """
    Example Page Object using the Page Object Model (POM) pattern.

    - Represents a generic "Example Form" page.
    - Methods are intentionally written to read like English when
      called from tests.

    HOW TO USE THIS TEMPLATE
    ------------------------
    - Copy this file and rename it to something like `login_page.py`.
    - Rename the class to `LoginPage`.
    - Replace `ExampleFormLocators` with your own locator class.
    """

    def open_example_form(self) -> None:
        """
        Navigate directly to the page's URL.

        - In real projects, you might pass a specific path segment
          to `self.open("/path")`.
        - Here we use the base_url only, assuming the example form
          is the landing page.
        """
        self.open()

    # =========================================================
    # FORM ACTIONS (NO ASSERTIONS HERE)
    # =========================================================

    def fill_name(self, name: str) -> None:
        """Fill the 'Name' field."""
        self.type_text(ExampleFormLocators.NAME_INPUT, name)

    def fill_email(self, email: str) -> None:
        """Fill the 'Email' field."""
        self.type_text(ExampleFormLocators.EMAIL_INPUT, email)

    def fill_message(self, message: str) -> None:
        """Fill the 'Message' text area."""
        self.type_text(ExampleFormLocators.MESSAGE_TEXTAREA, message)

    def submit_form(self) -> None:
        """Click the 'Submit' button."""
        self.click(ExampleFormLocators.SUBMIT_BUTTON)

    # =========================================================
    # GETTERS FOR ASSERTIONS IN TESTS
    # =========================================================

    def is_success_message_visible(self) -> bool:
        """
        Return True if a success message is visible, otherwise False.

        - The test file will ASSERT on this return value.
        """
        return self.is_visible(ExampleFormLocators.SUCCESS_MESSAGE)

    def get_success_message_text(self) -> str:
        """
        Get the text of the success message.

        - The test file may assert on this exact string.
        """
        return self.get_text(ExampleFormLocators.SUCCESS_MESSAGE)
