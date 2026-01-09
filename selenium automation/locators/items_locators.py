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


class ItemsPageLocators:
    """
    Locators for the Items page.

    - Replace these locators with real ones from your application.
    - This file is safe to copy and adapt for new pages.
    """

    SELECTED_SUPPLIER = (By.XPATH, "//div[contains(@class,'overflow-y-auto')]//ul/li[.//span[text()='SUPPLIER_NAME']]")
    EXPORT_POS_BUTTON = (By.XPATH, "//button[contains(@class,'bg-white') and normalize-space()='Export POS']")
    