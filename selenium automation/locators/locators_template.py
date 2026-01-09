"""
============================================================
 locators_template.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- TEMPLATE for storing Selenium locators separately from:
  - Page classes (actions and getters)
  - Test logic (assertions and flows)
  - Test data (input values and expectations)

WHAT YOU SHOULD EDIT
--------------------
- ADD NEW LOCATOR CLASSES for each page (e.g., LoginPageLocators).
- UPDATE LOCATOR VALUES to match your application's HTML.
  - Use the "UPDATE LOCATORS BELOW" section.

WHAT YOU SHOULD NOT EDIT
------------------------
- DO NOT place any test logic or assertions here.
- DO NOT instantiate WebDriver or interact with elements here.
"""

from selenium.webdriver.common.by import By


# ============================================================
# UPDATE LOCATORS BELOW
# ============================================================


class ExampleFormLocators:
    """
    Locators for the Example Form page.

    - Replace these locators with real ones from your application.
    - This file is safe to copy and adapt for new pages.
    """

    # TODO: UPDATE THESE SELECTORS TO MATCH YOUR REAL APPLICATION
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
