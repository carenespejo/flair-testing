"""
============================================================
 data_template.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- TEMPLATE for storing test data separately from:
  - Page classes (actions and getters)
  - Test logic (assertions and flows)
  - Locators (element selectors)

WHAT YOU SHOULD EDIT
--------------------
- INPUT TEST DATA HERE in the "TEST DATA" section.
- Create new data structures per feature or per test flow.

WHAT YOU SHOULD NOT EDIT
------------------------
- DO NOT import WebDriver, Page Objects, or PyTest here.
- DO NOT put assertions or test logic here.
  - This file is for VALUES only.
"""

from dataclasses import dataclass


# ============================================================
# TEST DATA
# ============================================================


@dataclass(frozen=True)
class ExampleFormData:
    """
    Example test data for the Example Form flow.

    - Copy this pattern for new forms or scenarios.
    """

    # TODO: INPUT TEST DATA HERE
    name: str = "Test User"
    email: str = "test.user@example.com"
    message: str = "This is a sample message for the contact form."
    expected_success_text: str = "Thank you for your message!"
