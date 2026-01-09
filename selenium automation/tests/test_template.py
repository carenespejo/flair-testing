# """
# ============================================================
#  test_template.py
# ============================================================

# WHAT THIS FILE IS FOR
# ----------------------
# - TEMPLATE for writing new PyTest-based Selenium tests.
# - Demonstrates:
#   - Using fixtures from `conftest.py` (e.g., `driver`, `base_url`).
#   - Using Page Objects for interactions.
#   - Keeping assertions and test logic in the test file ONLY.

# WHAT YOU SHOULD EDIT
# --------------------
# - RENAME the test function and descriptions to match your scenario.
# - USE your own Page Object classes instead of `ExampleFormPage`.
# - ADD more tests following the same structure.

# WHAT YOU SHOULD NOT EDIT
# ------------------------
# - DO NOT INITIALIZE WEBDRIVER HERE.
#   - Always use the `driver` fixture from `conftest.py`.
# - DO NOT PUT LOCATORS OR RAW XPATH/CSS SELECTORS HERE.
#   - Store them in the `locators` package instead.
# - DO NOT PUT TEST DATA VALUES HERE.
#   - Store them in the `data` package instead.
# """

# from __future__ import annotations

# from pages.page_template import ExampleFormPage
# from data.data_template import ExampleFormData


# def test_user_can_submit_example_form_and_see_success_message(driver, base_url):
#     """
#     This test is intentionally written to read like English.

#     GIVEN the user is on the Example Form page
#     WHEN the user fills in their name, email, and message
#     AND submits the form
#     THEN the user should see a success message confirming submission.
#     """

#     # Arrange: create page object and test data
#     page = ExampleFormPage(driver=driver, base_url=base_url)
#     data = ExampleFormData()

#     # Act: user opens the form and fills it out
#     page.open_example_form()
#     page.fill_name(data.name)
#     page.fill_email(data.email)
#     page.fill_message(data.message)
#     page.submit_form()

#     # Assert: user sees a success message
#     assert page.is_success_message_visible(), "Expected success message to be visible."

#     # (Optional) Assert exact success text
#     success_text = page.get_success_message_text()
#     assert data.expected_success_text in success_text, (
#         f"Expected success message to contain '{data.expected_success_text}', "
#         f"but got '{success_text}'."
#     )
