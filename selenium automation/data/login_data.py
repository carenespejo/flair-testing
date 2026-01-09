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
class LoginData:
    """
    Test data for the Login flow.

    - Copy this pattern for new forms or scenarios.
    """

    buyer_email: str = "direct@test.com"
    buyer_password: str = "Direct01@test.com"
    admin_email: str = "adminclerk01@test.com"
    admin_password: str = "Adminclerk01@test.com"
    
