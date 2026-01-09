from __future__ import annotations

import requests
import pytest
from pages.sourcing_page import SourcingPage
from pages.login_page import LoginPage
from data.source_data import supplier1, item2, edited_item2
from data.api_helper import ItemSourcingAPI
from data.login_data import LoginData

@pytest.mark.order(4)
def test_edit_item_successfully(driver, base_url):
    """
    GIVEN the user logs in to the application
    WHEN the user navigates to Sourcing and adds a new supplier with an item
    AND submits the form
    THEN the item should be saved and retrievable via API endpoint.
    """

    # ========== STEP 1: LOGIN ==========
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    # Login with your test credentials (adjust as needed)
    login_page.login(email=LoginData.buyer_email, password=LoginData.buyer_password)

    # ========== STEP 2: FILL AND SUBMIT SOURCING FORM ==========
    page = SourcingPage(driver=driver, base_url=base_url)
    data = item2
    edited_data = edited_item2
    supplier_data = supplier1

    page.open_sourcing_page()
    page.click_new_source_button()

    # Add and fill item details
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_edit_item_button_by_name(data.name)
    page.fill_item_name(edited_data.name)
    page.fill_item_description(edited_data.description)
    page.select_brand_option(edited_data.brand)
    page.select_department_option(edited_data.department)
    page.select_sub_department_option(edited_data.sub_department)
    page.select_category_option(edited_data.category)
    page.select_item_group_option(edited_data.item_group)
    page.select_style_option(edited_data.style)
    page.fill_selling_price(edited_data.selling_price)
    page.select_sell_unit_option(edited_data.sell_unit)
    page.select_purchase_unit_option(edited_data.purchase_unit)

    page.fill_barcode_stock_no(edited_data.barcode_stock_no)
    page.fill_barcode(edited_data.barcode)

    # Save the item
    page.click_update_item_button()

    # ========== STEP 3: RETRIEVE AUTH TOKEN FROM SESSION ==========
    # Get the auth token from browser cookies or localStorage
    auth_token = driver.execute_script("return localStorage.getItem('access_token') || sessionStorage.getItem('token')")

    # ========== STEP 4: VERIFY ITEM VIA API ==========
    api_base_url = base_url.replace("/sourcing", "").replace("/dashboard", "")  # Adjust if needed
    api = ItemSourcingAPI(base_url=api_base_url, auth_token=auth_token)

    # Verify supplier exists
    supplier_found = api.verify_supplier_created(supplier_data.supplier_name)
    assert supplier_found, f"Supplier '{supplier_data.supplier_name}' not found in API response"

    # Verify item was added to supplier
    item_found = api.verify_item_in_supplier(supplier_data.supplier_name, edited_data.name)
    assert item_found, f"Item '{edited_data.name}' not found under supplier '{supplier_data.supplier_name}'"

    print(f"✅ Item '{data.name}' successfully Edited to '{edited_data.name}' under supplier '{supplier_data.supplier_name}'")