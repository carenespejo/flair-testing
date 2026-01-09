from __future__ import annotations

import requests
from pages.sourcing_page import SourcingPage
from pages.login_page import LoginPage
from data.source_data import supplier1, item1
from data.api_helper import ItemSourcingAPI
from data.login_data import LoginData


def test_add_new_source_successfully(driver, base_url):
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
    item_list = [item1,item2,item3]
    supplier_data = supplier1
    item_data = item1

    page.open_sourcing_page()
    page.click_new_source_button()

    # Fill supplier information
    page.fill_supplier_name(supplier_data.supplier_name)
    page.fill_supplier_address(supplier_data.supplier_address)
    page.fill_contact_person(supplier_data.contact_person)
    page.fill_contact_address(supplier_data.contact_address)
    page.fill_contact_number(supplier_data.contact_number)
    page.fill_email(supplier_data.email)
    page.add_attachment(supplier_data.attachment_path)

    # Add and fill item details
    page.click_add_item_button()
    page.fill_item_name(item_data.name)
    page.fill_item_description(item_data.description)
    page.select_brand_option(item_data.brand)
    page.select_department_option(item_data.department)
    page.select_sub_department_option(item_data.sub_department)
    page.select_category_option(item_data.category)
    page.select_item_group_option(item_data.item_group)
    page.select_style_option(item_data.style)

    page.fill_selling_price(item_data.selling_price)
    page.select_selling_unit_option(item_data.selling_unit)
    page.select_purchase_unit_option(item_data.purchase_unit)
    page.fill_barcode_stock_no(item_data.barcode_stock_no)
    page.fill_barcode(item_data.barcode)
    # Save the item
    page.click_save_item_button()

    # ========== STEP 3: RETRIEVE AUTH TOKEN FROM SESSION ==========
    # Get the auth token from browser cookies or localStorage
    auth_token = driver.execute_script("return localStorage.getItem('access_token') || sessionStorage.getItem('token')")

    # ========== STEP 4: VERIFY VIA API ==========
    api_base_url = base_url.replace("/sourcing", "").replace("/dashboard", "")  # Adjust if needed
    api = ItemSourcingAPI(base_url=api_base_url, auth_token=auth_token)

    # Verify supplier was created
    supplier_found = api.verify_supplier_created(supplier_data.supplier_name)
    assert supplier_found, f"Supplier '{supplier_data.supplier_name}' not found in API response"

    # Verify item was added to supplier
    for item in item_list:
        item_found = api.verify_item_in_supplier(supplier_data.supplier_name, item.name)
        assert item_found, f"Item '{item.name}' not found under supplier '{supplier_data.supplier_name}'"

    print(f"✅ Supplier '{supplier_data.supplier_name}' created successfully")
    print(f"✅ Item '{item_data.name}' added to supplier")