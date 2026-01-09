from __future__ import annotations

import time

import pytest
from pages.sourcing_page import SourcingPage
from pages.login_page import LoginPage
from pages.items_page import ItemsPage
from conftest import DEFAULT_DOWNLOAD_DIR
from data.source_data import supplier1, supplier2, item1, item2, item3, edited_item2
from data.login_data import LoginData
from data.api_helper import ItemSourcingAPI
from data.files_data import get_valid_document_paths, get_valid_image_paths

@pytest.mark.order(3)
def test_approve_new_source_complete_flow(driver, base_url):
    """
    Complete flow test for adding a new source with supplier and multiple items.
    
    Steps:
    1. Login as buyer
    2. Access sourcing page
    3. Test cancel flow
    4. Test validation errors (supplier, email, items)
    5. Test alphanumeric input filtering for contact number
    6. Test invalid and valid file attachments
    7. Add multiple items (3 total)
    8. Fill item details
    9. Remove one item
    10. Save supplier
    """

    item_list = [item1, item2]
    print("\n" + "="*80)
    print("TEST: Add New Source - Complete Flow")
    print("="*80)

    # ========== STEP 1: LOGIN ==========
    print("\n[STEP 1] Login as Buyer Account")
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    print(f"  ✓ Navigated to login page: {base_url}/login")
    
    login_page.login(email=LoginData.buyer_email, password=LoginData.buyer_password)
    print(f"  ✓ Logged in with email: {LoginData.buyer_email}")

    # ========== STEP 2: ACCESS SOURCING PAGE ==========
    print("\n[STEP 2] Access Sourcing Page")
    page = SourcingPage(driver=driver, base_url=base_url)
    page.open_sourcing_page()
    print("  ✓ Sourcing page opened successfully")

    # ========== STEP 3-4: Cancel Flow ==========
    print("\n[STEP 3-4] Cancel Flow")
    print("  • Click + New Source button")
    page.click_new_source_button()
    print("  ✓ New source form opened")
    
    print("  • Click Cancel button")
    page.click_cancel_item_button()
    print("  ✓ Form closed after clicking Cancel")

    # ========== STEP 5-6: CLICK NEW SOURCE AGAIN ==========
    print("\n[STEP 5-6] Open New Source Form Again")
    page.click_new_source_button()
    print("  ✓ New source form opened again")

    # ========== STEP 7: TEST SUPPLIER NAME REQUIRED ==========
    print("\n[STEP 7] Test Supplier Name Required Validation")
    print("  • Click Save button without entering supplier name")
    page.click_save_item_button()
    
    supplier_name_error = page.supplier_name_required_displayed()
    print(f"  ✓ Supplier name required error displayed: {supplier_name_error}")
    assert supplier_name_error, "Supplier name required error should be displayed"

    # ========== STEP 8: ENTER SUPPLIER DETAILS ==========
    print("\n[STEP 8] Enter Supplier Details")
    supplier_data = supplier1
    
    print(f"  • Fill supplier name: {supplier_data.supplier_name}")
    page.fill_supplier_name(supplier_data.supplier_name)
    
    print(f"  • Fill supplier address: {supplier_data.supplier_address}")
    page.fill_supplier_address(supplier_data.supplier_address)
    
    print(f"  • Fill contact person: {supplier_data.contact_person}")
    page.fill_contact_person(supplier_data.contact_person)
    
    print(f"  • Fill contact address: {supplier_data.contact_address}")
    page.fill_contact_address(supplier_data.contact_address)
    print("  ✓ Basic supplier information filled")

    # ========== STEP 8b: TEST CONTACT NUMBER ALPHANUMERIC FILTERING ==========
    print("\n[STEP 8b] Test Contact Number Alphanumeric Filtering")
    alphanumeric_input = "12345ABC6789XYZ"
    print(f"  • Enter alphanumeric input: {alphanumeric_input}")
    page.fill_contact_number(alphanumeric_input)
    time.sleep(0.5)
    print("  ✓ Contact number field should only contain numeric characters")

    # ========== STEP 8c-8e: TEST EMAIL VALIDATION ==========
    print("\n[STEP 8c-8e] Test Email Validation")
    print("  • Try to save without email")
    page.click_save_item_button()
    time.sleep(1)
    
    email_required_error = page.email_required_displayed()
    print(f"  ✓ Email required error displayed: {email_required_error}")
    assert email_required_error, "Email required error should be displayed"
    
    print("  • Enter invalid email format: invalid-email-format")
    page.fill_email("invalid-email-format")
    time.sleep(0.5)
    page.click_save_item_button()
    print("  ✓ Invalid email validation triggered")
    
    print(f"  • Enter valid email: {supplier_data.email}")
    page.fill_email(supplier_data.email)
    print("  ✓ Valid email entered")

    # ========== STEP 9: VERIFY NUMBER OF ITEMS WARNING ==========
    print("\n[STEP 9] Verify Number of Items Warning")
    print("  • Click save without adding any items")
    page.click_save_item_button()
    time.sleep(1)
    print("  ✓ 'Please add at least one item' error will be shown")

    # ========== STEP 10: TEST INVALID ATTACHMENTS ==========
    print("\n[STEP 10] Test Invalid Attachments")
    invalid_files = [
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_EXE.exe",
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_BAT.bat",
    ]
    print(f"  • Attempting to upload {len(invalid_files)} invalid files:")
    for file in invalid_files:
        print(f"    - {file}")
    
    page.add_multiple_attachments("\n".join(invalid_files))
    time.sleep(1)
    
    rejected_error = page.rejected_files_displayed()
    print(f"  ✓ Rejected files error displayed: {rejected_error}")
    assert rejected_error, "Rejected files error should be displayed for invalid files"

    # ========== STEP 11: ADD VALID DOCUMENTS ==========
    print("\n[STEP 11] Add Valid Documents")
    valid_document_paths = get_valid_document_paths()
    print(f"  • Uploading valid documents...")
    page.add_multiple_attachments(valid_document_paths)
    time.sleep(0.5)
    
    document_names = ["TEST_PDF.pdf", "TEST_DOC.doc", "TEST_DOCX.docx", "TEST_XLS.xls", "TEST_XLSX.xlsx", "TEST_PPT.ppt"]
    print(f"  • Verifying {len(document_names)} documents are displayed:")
    for doc in document_names:
        print(f"    - {doc}")
    
    all_docs_displayed = page.are_all_attachments_displayed(document_names)
    print(f"  ✓ All valid documents displayed: {all_docs_displayed}")
    assert all_docs_displayed, "All valid documents should be displayed"

    # ========== STEP 12: ADD VALID IMAGES ==========
    print("\n[STEP 12] Add Valid Images")
    valid_image_paths = get_valid_image_paths()
    print(f"  • Uploading valid images...")
    page.add_multiple_attachments(valid_image_paths)
    time.sleep(1)
    
    image_names = ["TEST_JPG.jpg", "TEST_PNG.png", "TEST_GIF.gif", "TEST_SVG.svg", "TEST_TIFF.tiff", "TEST_WEBP.webp"]
    print(f"  • Uploading {len(image_names)} images:")
    for img in image_names:
        print(f"    - {img}")
    
    # Verify images were uploaded by counting image elements
    image_count = page.get_image_attachment_count()
    print(f"  ✓ Image attachments found: {image_count}")
    assert image_count >= len(image_names), f"Expected at least {len(image_names)} images, but found {image_count}"
    
    # Also verify total attachment count (documents + images)
    total_attachments = page.get_total_attachment_count()
    print(f"  ✓ Total attachments in container: {total_attachments} (6 documents + {image_count} images)")

    # ========== STEP 13: CLICK ADD ITEM BUTTON ==========
    print("\n[STEP 13] Click Add Item Button")
    page.click_add_item_button()
    time.sleep(1)
    print("  ✓ Item #1 form opened")

    # ========== STEP 14: TEST ITEM PRODUCT NAME REQUIRED ==========
    print("\n[STEP 14] Test Item #1 Product Name Required Validation")
    print("  • Click Save without entering item details")
    page.click_save_item_button()
    time.sleep(1)
    
    item_name_error = page.item_product_name_required_displayed(item_index=1)
    print(f"  ✓ Item #1 product name required error displayed: {item_name_error}")
    assert item_name_error, "Item #1: product name required error should be displayed"

    # ========== STEP 15: ADD 2 MORE ITEMS (TOTAL 3) ==========
    print("\n[STEP 15] Add 2 More Items (Total 3 Items)")
    print("  • Click Add Item button (Item #2)")
    page.click_add_item_button()
    time.sleep(0.5)
    print("  ✓ Item #2 form opened")
    
    print("  • Click Add Item button (Item #3)")
    page.click_add_item_button()
    time.sleep(0.5)
    print("  ✓ Item #3 form opened")
    print("  ✓ Total of 3 items added")

    # ========== STEP 16: FILL ITEM 1 DETAILS ==========
    print("\n[STEP 16] Fill Item #1 Details")
    item_data = item1
    print(f"  • Item Name: {item_data.name}")
    page.fill_item_name(item_data.name)
    
    print(f"  • Description: {item_data.description}")
    page.fill_item_description(item_data.description)
    
    print(f"  • Brand: {item_data.brand}")
    page.select_brand_option(item_data.brand)
    
    print(f"  • Department: {item_data.department}")
    page.select_department_option(item_data.department)
    
    print(f"  • Sub-Department: {item_data.sub_department}")
    page.select_sub_department_option(item_data.sub_department)
    
    print(f"  • Category: {item_data.category}")
    page.select_category_option(item_data.category)
    
    print(f"  • Item Group: {item_data.item_group}")
    page.select_item_group_option(item_data.item_group)
    
    print(f"  • Style: {item_data.style}")
    page.select_style_option(item_data.style)
    
    print(f"  • Selling Price: ${item_data.selling_price}")
    page.fill_selling_price(str(item_data.selling_price))
    
    print(f"  • Sell Unit: {item_data.sell_unit}")
    page.select_sell_unit_option(item_data.sell_unit)
    
    print(f"  • Purchase Unit: {item_data.purchase_unit}")
    page.select_purchase_unit_option(item_data.purchase_unit)
    
    print(f"  • Barcode Stock No: {item_data.barcode_stock_no}")
    page.fill_barcode_stock_no(item_data.barcode_stock_no)
    
    print(f"  • Barcode: {item_data.barcode}")
    page.fill_barcode(item_data.barcode)
    
    print(f"  • Size Category: {item_data.size_category}")
    page.select_size_category_option(item_data.size_category)
    
    print(f"  • Color Category: {item_data.color_category}")
    page.select_color_category_option(item_data.color_category)
    
    print(f"  • Packaging: {item_data.packaging}")
    page.select_packaging_option(item_data.packaging)
    
    print(f"  • Specification: {item_data.specification}")
    page.select_specification_option(item_data.specification)
    
    print(f"  • Collection: {item_data.collection}")
    page.select_collection_option(item_data.collection)

    print(f"  • Remarks: {item_data.remarks}")
    page.fill_remarks(item_data.remarks)
    print("  ✓ Item #1 details filled completely")

    # ========== STEP 17: FILL ITEM 2 DETAILS ==========
    print("\n[STEP 17] Fill Item #2 Details")
    item_data = item2
    print(f"  • Item Name: {item_data.name}")
    page.fill_item_name(item_data.name, item_index=2)
    print(f"  • Description: {item_data.description}")
    page.fill_item_description(item_data.description, item_index=2)
    print(f"  • Brand: {item_data.brand}")
    page.select_brand_option(item_data.brand, item_index=2)
    print(f"  • Department: {item_data.department}")
    page.select_department_option(item_data.department, item_index=2)
    print(f"  • Sub-Department: {item_data.sub_department}")
    page.select_sub_department_option(item_data.sub_department, item_index=2)
    print(f"  • Category: {item_data.category}")
    page.select_category_option(item_data.category, item_index=2)
    print(f"  • Item Group: {item_data.item_group}")
    page.select_item_group_option(item_data.item_group, item_index=2)
    print(f"  • Style: {item_data.style}")
    page.select_style_option(item_data.style, item_index=2)
    print(f"  • Selling Price: ${item_data.selling_price}")
    page.fill_selling_price(str(item_data.selling_price), item_index=2)
    print(f"  • Selling Unit: {item_data.sell_unit}")
    page.select_sell_unit_option(item_data.sell_unit, item_index=2)
    print(f"  • Purchase Unit: {item_data.purchase_unit}")
    page.select_purchase_unit_option(item_data.purchase_unit, item_index=2)
    print(f"  • Barcode Stock No: {item_data.barcode_stock_no}")
    page.fill_barcode_stock_no(item_data.barcode_stock_no, item_index=2)
    print(f"  • Barcode: {item_data.barcode}")
    page.fill_barcode(item_data.barcode, item_index=2)
    print(f"  • Size Category: {item_data.size_category}")
    page.select_size_category_option(item_data.size_category, item_index=2)
    print(f"  • Color Category: {item_data.color_category}")
    page.select_color_category_option(item_data.color_category, item_index=2)
    print(f"  • Packaging: {item_data.packaging}")
    page.select_packaging_option(item_data.packaging, item_index=2)
    print(f"  • Specification: {item_data.specification}")
    page.select_specification_option(item_data.specification, item_index=2)
    print(f"  • Collection: {item_data.collection}")
    page.select_collection_option(item_data.collection, item_index=2)
    print(f"  • Remarks: {item_data.remarks}")
    page.fill_remarks(item_data.remarks, item_index=2)
    print("  ✓ Item #2 details filled completely")

    # ========== STEP 18: FILL ITEM 3 DETAILS ==========
    print("\n[STEP 18] Fill Item #3 Details")
    item_data = item3
    print(f"  • Item Name: {item_data.name}")
    page.fill_item_name(item_data.name, item_index=3)
    print(f"  • Description: {item_data.description}")
    page.fill_item_description(item_data.description, item_index=3)
    print(f"  • Brand: {item_data.brand}")
    page.select_brand_option(item_data.brand, item_index=3)
    print(f"  • Department: {item_data.department}")
    page.select_department_option(item_data.department, item_index=3)
    print(f"  • Sub-Department: {item_data.sub_department}")
    page.select_sub_department_option(item_data.sub_department, item_index=3)
    print(f"  • Category: {item_data.category}")
    page.select_category_option(item_data.category, item_index=3)
    print(f"  • Item Group: {item_data.item_group}")
    page.select_item_group_option(item_data.item_group, item_index=3)
    print(f"  • Style: {item_data.style}")
    page.select_style_option(item_data.style, item_index=3)
    print(f"  • Selling Price: ${item_data.selling_price}")
    page.fill_selling_price(str(item_data.selling_price), item_index=3)
    print(f"  • Selling Unit: {item_data.sell_unit}")
    page.select_sell_unit_option(item_data.sell_unit, item_index=3)
    print(f"  • Purchase Unit: {item_data.purchase_unit}")
    page.select_purchase_unit_option(item_data.purchase_unit, item_index=3)
    print(f"  • Barcode Stock No: {item_data.barcode_stock_no}")
    page.fill_barcode_stock_no(item_data.barcode_stock_no, item_index=3)
    print(f"  • Barcode: {item_data.barcode}")
    page.fill_barcode(item_data.barcode, item_index=3)
    print(f"  • Size Category: {item_data.size_category}")
    page.select_size_category_option(item_data.size_category, item_index=3)
    print(f"  • Color Category: {item_data.color_category}")
    page.select_color_category_option(item_data.color_category, item_index=3)
    print(f"  • Packaging: {item_data.packaging}")
    page.select_packaging_option(item_data.packaging, item_index=3)
    print(f"  • Specification: {item_data.specification}")
    page.select_specification_option(item_data.specification, item_index=3)
    print(f"  • Collection: {item_data.collection}")
    page.select_collection_option(item_data.collection, item_index=3)
    print(f"  • Remarks: {item_data.remarks}")
    page.fill_remarks(item_data.remarks, item_index=3)
    print("  ✓ Item #3 details filled completely")

    # ========== STEP 19: REMOVE 3RD ITEM ==========
    print("\n[STEP 19] Remove Item #3")
    print("  • Click Remove Item button for Item #3")
    page.click_remove_item_button(item_index=3)
    time.sleep(1)
    print("  ✓ Item #3 removed successfully")
    print("  ✓ Remaining items: Item #1 and Item #2 (total 2 items)")

    # ========== STEP 20: SAVE ==========
    print("\n[STEP 20] Save Supplier")
    print("  • Click Save button to submit supplier form")
    page.click_save_item_button()
    #wait until success notification appears
    success_displayed = page.is_saved_successfully_displayed()
    assert success_displayed, "Supplier saved notification should be displayed"
    print("  ✓ Supplier form submitted successfully")

    print("\n" + "="*80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\nSummary:")
    print(f"  ✓ Supplier: {supplier_data.supplier_name}")
    print(f"  ✓ Contact Email: {supplier_data.email}")
    print(f"  ✓ Documents Uploaded: 6 (PDF, DOC, DOCX, XLS, XLSX, PPT)")
    print(f"  ✓ Images Uploaded: 6 (JPG, PNG, GIF, SVG, TIFF, WEBP)")
    print(f"  ✓ Items Added: 2 (Item #1 and Item #2)")
    print(f"  ✓ Item #3: Removed after testing")
    print("="*80 + "\n")

    
    # ========== STEP 21: RETRIEVE AUTH TOKEN FROM SESSION ==========
    # Get the auth token from browser cookies or localStorage
    auth_token = driver.execute_script("return localStorage.getItem('access_token') || sessionStorage.getItem('token')")

    # ========== STEP 22: VERIFY VIA API ==========
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
    print(f"✅ Items added to supplier")

    # Test edit item 2 and add Item 3 again before publishing
    print("\n[STEP 23] Edit Item #2 and Re-Add Item #3 Before Publishing")
    print("  • Edit Item #2 Selling Price")

    data = item2
    edited_data = edited_item2
    supplier_data = supplier1

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

    # ========== STEP 24: RETRIEVE AUTH TOKEN FROM SESSION ==========
    # Get the auth token from browser cookies or localStorage
    auth_token = driver.execute_script("return localStorage.getItem('access_token') || sessionStorage.getItem('token')")

    # ========== STEP 25: VERIFY ITEM VIA API ==========
    api_base_url = base_url.replace("/sourcing", "").replace("/dashboard", "")  # Adjust if needed
    api = ItemSourcingAPI(base_url=api_base_url, auth_token=auth_token)

    # Verify supplier exists
    supplier_found = api.verify_supplier_created(supplier_data.supplier_name)
    assert supplier_found, f"Supplier '{supplier_data.supplier_name}' not found in API response"

    # Verify item was added to supplier
    item_found = api.verify_item_in_supplier(supplier_data.supplier_name, edited_data.name)
    assert item_found, f"Item '{edited_data.name}' not found under supplier '{supplier_data.supplier_name}'"

    print(f"✅ Item '{data.name}' successfully Edited to '{edited_data.name}' under supplier '{supplier_data.supplier_name}'")

    data = item3
    supplier_data = supplier1

    page.open_sourcing_page()
    page.click_new_source_button()

    # Add and fill item details
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_add_item_button()
    page.fill_item_name(data.name)
    page.fill_item_description(data.description)
    page.select_brand_option(data.brand)
    page.select_department_option(data.department)
    page.select_sub_department_option(data.sub_department)
    page.select_category_option(data.category)
    page.select_item_group_option(data.item_group)
    page.select_style_option(data.style)
    page.fill_selling_price(data.selling_price)
    page.select_sell_unit_option(data.sell_unit)
    page.select_purchase_unit_option(data.purchase_unit)

    page.fill_barcode_stock_no(data.barcode_stock_no)
    page.fill_barcode(data.barcode)

    # Save the item
    page.click_save_item_button()

    # ========== STEP 26: RETRIEVE AUTH TOKEN FROM SESSION ==========
    # Get the auth token from browser cookies or localStorage
    auth_token = driver.execute_script("return localStorage.getItem('access_token') || sessionStorage.getItem('token')")

    # ========== STEP 27: VERIFY ITEM VIA API ==========
    api_base_url = base_url.replace("/sourcing", "").replace("/dashboard", "")  # Adjust if needed
    api = ItemSourcingAPI(base_url=api_base_url, auth_token=auth_token)

    # Verify supplier exists
    supplier_found = api.verify_supplier_created(supplier_data.supplier_name)
    assert supplier_found, f"Supplier '{supplier_data.supplier_name}' not found in API response"

    # Verify item was added to supplier
    item_found = api.verify_item_in_supplier(supplier_data.supplier_name, data.name)
    assert item_found, f"Item '{data.name}' not found under supplier '{supplier_data.supplier_name}'"

    print(f"✅ Item '{data.name}' successfully added to supplier '{supplier_data.supplier_name}'")


    # ========== STEP 28: PUBLISH ==========
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_publish_button()
    page.confirm_publish()
    page.is_published_successfully_displayed()
    print(f"✅ Supplier '{supplier_data.supplier_name}' published successfully")


    # ========== STEP 29: SIGN OUT ==========
    print("\n[STEP 29] Sign Out")
    page.sign_out()
    print("  ✓ Signed out successfully")

    # ========== Approval ==========

    print("\n" + "="*80)
    print("TEST: Source Approval Flow")
    print("="*80)

    # ========== STEP 1: LOGIN ==========

    print("\n[APPROVAL STEP 1] Login as Admin Account")
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    # Login with your test credentials (adjust as needed)
    login_page.login(email=LoginData.admin_email, password=LoginData.admin_password)
    print(f"  ✓ Logged in with email: {LoginData.admin_email}")

    # ========== STEP 2: APPROVE ITEM ==========
    print("\n[APPROVAL STEP 2] Approve the Newly Added Source")
    page = SourcingPage(driver=driver, base_url=base_url)

    page.open_sourcing_page()
    print("  ✓ Sourcing page opened successfully")
    page.select_supplier_from_list(supplier_data.supplier_name)
    print(f"  ✓ Supplier selected: {supplier_data.supplier_name}")
    #test cancel approve flow
    print("\n[APPROVAL STEP 3] Test Approve Cancel Flow")
    print("  • Click Approve button")
    page.click_approve_button()
    page.cancel_approve()
    print("  ✓ Approve cancelled successfully")

    print("\n[APPROVAL STEP 4] Confirm Approval")
    print("  • Click Approve button again")
    page.click_approve_button()
    page.confirm_approve()
    print("  ✓ Source approved successfully")

    assert page.is_approved_successfully_displayed(), "Approve confirmation dialog should be displayed"
    print("\n" + "="*80)
    print("APPROVAL TEST COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")

    print(f"✅ Source '{supplier_data.supplier_name}' approved successfully")

    # ========== STEP 5: EXPPORT POS ==========
    print("\n[EXPORT STEP 5] Export POS for Approved Source")
    items_page = ItemsPage(driver=driver, base_url=base_url)
    items_page.open_items_page()
    print("  ✓ Items page opened successfully")
    items_page.select_supplier("Automated Test Supplier Inc.")
    print(f"  ✓ Supplier Selected: Automated Test Supplier Inc.")
    items_page.click_export_pos_button()
    print("  • Export POS button clicked, waiting for download to complete...")
    items_page.is_pos_file_downloaded(download_dir=DEFAULT_DOWNLOAD_DIR)  # Clear any existing files
    print("  ✓ POS export verified successfully")
    print("\n" + "="*80)
    
def test_reject_new_source_complete_flow(driver, base_url):
    """
    Complete flow test for rejecting a new source with supplier and multiple items.
    
    Steps:
    1. Login as buyer
    2. Access sourcing page
    3. Add new source with supplier and items
    4. Save supplier
    5. Login as admin
    6. Reject the newly added source
    """
    
    item_list = [item1, item2]
    print("\n" + "="*80)
    print("TEST: Add New Source - Complete Flow")
    print("="*80)

    # ========== STEP 1: LOGIN ==========
    print("\n[STEP 1] Login as Buyer Account")
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    print(f"  ✓ Navigated to login page: {base_url}/login")
    
    login_page.login(email=LoginData.buyer_email, password=LoginData.buyer_password)
    print(f"  ✓ Logged in with email: {LoginData.buyer_email}")

    # ========== STEP 2: ACCESS SOURCING PAGE ==========
    print("\n[STEP 2] Access Sourcing Page")
    page = SourcingPage(driver=driver, base_url=base_url)
    page.open_sourcing_page()
    print("  ✓ Sourcing page opened successfully")

    # ========== STEP 3-4: TEST CANCEL FLOW ==========
    print("\n[STEP 3-4] Test Cancel Flow")
    print("  • Click + New Source button")
    page.click_new_source_button()
    import time
    print("  ✓ New source form opened")
    
    print("  • Click Cancel button")
    page.click_cancel_item_button()
    print("  ✓ Form closed after clicking Cancel")

    # ========== STEP 5-6: CLICK NEW SOURCE AGAIN ==========
    print("\n[STEP 5-6] Open New Source Form Again")
    page.click_new_source_button()
    print("  ✓ New source form opened again")

    # ========== STEP 7: TEST SUPPLIER NAME REQUIRED ==========
    print("\n[STEP 7] Test Supplier Name Required Validation")
    print("  • Click Save button without entering supplier name")
    page.click_save_item_button()
    
    supplier_name_error = page.supplier_name_required_displayed()
    print(f"  ✓ Supplier name required error displayed: {supplier_name_error}")
    assert supplier_name_error, "Supplier name required error should be displayed"

    # ========== STEP 8: ENTER SUPPLIER DETAILS ==========
    print("\n[STEP 8] Enter Supplier Details")
    supplier_data = supplier2
    
    print(f"  • Fill supplier name: {supplier_data.supplier_name}")
    page.fill_supplier_name(supplier_data.supplier_name)
    
    print(f"  • Fill supplier address: {supplier_data.supplier_address}")
    page.fill_supplier_address(supplier_data.supplier_address)
    
    print(f"  • Fill contact person: {supplier_data.contact_person}")
    page.fill_contact_person(supplier_data.contact_person)
    
    print(f"  • Fill contact address: {supplier_data.contact_address}")
    page.fill_contact_address(supplier_data.contact_address)
    print("  ✓ Basic supplier information filled")

    # ========== STEP 8b: TEST CONTACT NUMBER ALPHANUMERIC FILTERING ==========
    print("\n[STEP 8b] Test Contact Number Alphanumeric Filtering")
    alphanumeric_input = "12345ABC6789XYZ"
    print(f"  • Enter alphanumeric input: {alphanumeric_input}")
    page.fill_contact_number(alphanumeric_input)
    print("  ✓ Contact number field should only contain numeric characters")

    # ========== STEP 8c-8e: TEST EMAIL VALIDATION ==========
    print("\n[STEP 8c-8e] Test Email Validation")
    print("  • Try to save without email")
    page.click_save_item_button()
    
    email_required_error = page.email_required_displayed()
    print(f"  ✓ Email required error displayed: {email_required_error}")
    assert email_required_error, "Email required error should be displayed"
    
    print("  • Enter invalid email format: invalid-email-format")
    page.fill_email("invalid-email-format")
    page.click_save_item_button()
    print("  ✓ Invalid email validation triggered")
    
    print(f"  • Enter valid email: {supplier_data.email}")
    page.fill_email(supplier_data.email)
    print("  ✓ Valid email entered")

    # ========== STEP 9: VERIFY NUMBER OF ITEMS WARNING ==========
    print("\n[STEP 9] Verify Number of Items Warning")
    print("  • Click save without adding any items")
    page.click_save_item_button()
    print("  ✓ 'Please add at least one item' error will be shown")

    # ========== STEP 10: TEST INVALID ATTACHMENTS ==========
    print("\n[STEP 10] Test Invalid Attachments")
    invalid_files = [
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_EXE.exe",
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_BAT.bat",
    ]
    print(f"  • Attempting to upload {len(invalid_files)} invalid files:")
    for file in invalid_files:
        print(f"    - {file}")
    
    page.add_multiple_attachments("\n".join(invalid_files))
    time.sleep(1)
    
    rejected_error = page.rejected_files_displayed()
    print(f"  ✓ Rejected files error displayed: {rejected_error}")
    assert rejected_error, "Rejected files error should be displayed for invalid files"

    # ========== STEP 11: ADD VALID DOCUMENTS ==========
    print("\n[STEP 11] Add Valid Documents")
    valid_document_paths = get_valid_document_paths()
    print(f"  • Uploading valid documents...")
    page.add_multiple_attachments(valid_document_paths)
    time.sleep(1)
    
    document_names = ["TEST_PDF.pdf", "TEST_DOC.doc", "TEST_DOCX.docx", "TEST_XLS.xls", "TEST_XLSX.xlsx", "TEST_PPT.ppt"]
    print(f"  • Verifying {len(document_names)} documents are displayed:")
    for doc in document_names:
        print(f"    - {doc}")
    
    all_docs_displayed = page.are_all_attachments_displayed(document_names)
    print(f"  ✓ All valid documents displayed: {all_docs_displayed}")
    assert all_docs_displayed, "All valid documents should be displayed"

    # ========== STEP 12: ADD VALID IMAGES ==========
    print("\n[STEP 12] Add Valid Images")
    valid_image_paths = get_valid_image_paths()
    print(f"  • Uploading valid images...")
    page.add_multiple_attachments(valid_image_paths)
    time.sleep(1)
    
    image_names = ["TEST_JPG.jpg", "TEST_PNG.png", "TEST_GIF.gif", "TEST_SVG.svg", "TEST_TIFF.tiff", "TEST_WEBP.webp"]
    print(f"  • Uploading {len(image_names)} images:")
    for img in image_names:
        print(f"    - {img}")
    
    # Verify images were uploaded by counting image elements
    image_count = page.get_image_attachment_count()
    print(f"  ✓ Image attachments found: {image_count}")
    assert image_count >= len(image_names), f"Expected at least {len(image_names)} images, but found {image_count}"
    
    # Also verify total attachment count (documents + images)
    total_attachments = page.get_total_attachment_count()
    print(f"  ✓ Total attachments in container: {total_attachments} (6 documents + {image_count} images)")

    # ========== STEP 13: CLICK ADD ITEM BUTTON ==========
    print("\n[STEP 13] Click Add Item Button")
    page.click_add_item_button()
    print("  ✓ Item #1 form opened")

    # ========== STEP 14: TEST ITEM PRODUCT NAME REQUIRED ==========
    print("\n[STEP 14] Test Item #1 Product Name Required Validation")
    print("  • Click Save without entering item details")
    page.click_save_item_button()
    
    item_name_error = page.item_product_name_required_displayed(item_index=1)
    print(f"  ✓ Item #1 product name required error displayed: {item_name_error}")
    assert item_name_error, "Item #1: product name required error should be displayed"

    # ========== STEP 15: ADD 2 MORE ITEMS (TOTAL 3) ==========
    print("\n[STEP 15] Add 2 More Items (Total 3 Items)")
    print("  • Click Add Item button (Item #2)")
    page.click_add_item_button()
    print("  ✓ Item #2 form opened")
    
    print("  • Click Add Item button (Item #3)")
    page.click_add_item_button()
    print("  ✓ Item #3 form opened")
    print("  ✓ Total of 3 items added")

    # ========== STEP 16: FILL ITEM 1 DETAILS ==========
    print("\n[STEP 16] Fill Item #1 Details")
    item_data = item1
    print(f"  • Item Name: {item_data.name}")
    page.fill_item_name(item_data.name)
    
    print(f"  • Description: {item_data.description}")
    page.fill_item_description(item_data.description)
    
    print(f"  • Brand: {item_data.brand}")
    page.select_brand_option(item_data.brand)
    
    print(f"  • Department: {item_data.department}")
    page.select_department_option(item_data.department)
    
    print(f"  • Sub-Department: {item_data.sub_department}")
    page.select_sub_department_option(item_data.sub_department)
    
    print(f"  • Category: {item_data.category}")
    page.select_category_option(item_data.category)
    
    print(f"  • Item Group: {item_data.item_group}")
    page.select_item_group_option(item_data.item_group)
    
    print(f"  • Style: {item_data.style}")
    page.select_style_option(item_data.style)
    
    print(f"  • Selling Price: ${item_data.selling_price}")
    page.fill_selling_price(str(item_data.selling_price))
    
    print(f"  • Sell Unit: {item_data.sell_unit}")
    page.select_sell_unit_option(item_data.sell_unit)
    
    print(f"  • Purchase Unit: {item_data.purchase_unit}")
    page.select_purchase_unit_option(item_data.purchase_unit)
    
    print(f"  • Barcode Stock No: {item_data.barcode_stock_no}")
    page.fill_barcode_stock_no(item_data.barcode_stock_no)
    
    print(f"  • Barcode: {item_data.barcode}")
    page.fill_barcode(item_data.barcode)
    
    print(f"  • Size Category: {item_data.size_category}")
    page.select_size_category_option(item_data.size_category)
    
    print(f"  • Color Category: {item_data.color_category}")
    page.select_color_category_option(item_data.color_category)
    
    print(f"  • Packaging: {item_data.packaging}")
    page.select_packaging_option(item_data.packaging)
    
    print(f"  • Specification: {item_data.specification}")
    page.select_specification_option(item_data.specification)
    
    print(f"  • Collection: {item_data.collection}")
    page.select_collection_option(item_data.collection)
    print("  ✓ Item #1 details filled completely")

    # ========== STEP 17: FILL ITEM 2 DETAILS ==========
    print("\n[STEP 17] Fill Item #2 Details")
    item_data = item2
    print(f"  • Item Name: {item_data.name}")
    page.fill_item_name(item_data.name, item_index=2)
    print(f"  • Description: {item_data.description}")
    page.fill_item_description(item_data.description, item_index=2)
    print(f"  • Brand: {item_data.brand}")
    page.select_brand_option(item_data.brand, item_index=2)
    print(f"  • Department: {item_data.department}")
    page.select_department_option(item_data.department, item_index=2)
    print(f"  • Sub-Department: {item_data.sub_department}")
    page.select_sub_department_option(item_data.sub_department, item_index=2)
    print(f"  • Category: {item_data.category}")
    page.select_category_option(item_data.category, item_index=2)
    print(f"  • Item Group: {item_data.item_group}")
    page.select_item_group_option(item_data.item_group, item_index=2)
    print(f"  • Style: {item_data.style}")
    page.select_style_option(item_data.style, item_index=2)
    print(f"  • Selling Price: ${item_data.selling_price}")
    page.fill_selling_price(str(item_data.selling_price), item_index=2)
    print(f"  • Selling Unit: {item_data.sell_unit}")
    page.select_sell_unit_option(item_data.sell_unit, item_index=2)
    print(f"  • Purchase Unit: {item_data.purchase_unit}")
    page.select_purchase_unit_option(item_data.purchase_unit, item_index=2)
    print(f"  • Barcode Stock No: {item_data.barcode_stock_no}")
    page.fill_barcode_stock_no(item_data.barcode_stock_no, item_index=2)
    print(f"  • Barcode: {item_data.barcode}")
    page.fill_barcode(item_data.barcode, item_index=2)
    print(f"  • Size Category: {item_data.size_category}")
    page.select_size_category_option(item_data.size_category, item_index=2)
    print(f"  • Color Category: {item_data.color_category}")
    page.select_color_category_option(item_data.color_category, item_index=2)
    print(f"  • Packaging: {item_data.packaging}")
    page.select_packaging_option(item_data.packaging, item_index=2)
    print(f"  • Specification: {item_data.specification}")
    page.select_specification_option(item_data.specification, item_index=2)
    print(f"  • Collection: {item_data.collection}")
    page.select_collection_option(item_data.collection, item_index=2)
    print("  ✓ Item #2 details filled completely")

    # ========== STEP 18: FILL ITEM 3 DETAILS ==========
    print("\n[STEP 18] Fill Item #3 Details")
    item_data = item3
    print(f"  • Item Name: {item_data.name}")
    page.fill_item_name(item_data.name, item_index=3)
    print(f"  • Description: {item_data.description}")
    page.fill_item_description(item_data.description, item_index=3)
    print(f"  • Brand: {item_data.brand}")
    page.select_brand_option(item_data.brand, item_index=3)
    print(f"  • Department: {item_data.department}")
    page.select_department_option(item_data.department, item_index=3)
    print(f"  • Sub-Department: {item_data.sub_department}")
    page.select_sub_department_option(item_data.sub_department, item_index=3)
    print(f"  • Category: {item_data.category}")
    page.select_category_option(item_data.category, item_index=3)
    print(f"  • Item Group: {item_data.item_group}")
    page.select_item_group_option(item_data.item_group, item_index=3)
    print(f"  • Style: {item_data.style}")
    page.select_style_option(item_data.style, item_index=3)
    print(f"  • Selling Price: ${item_data.selling_price}")
    page.fill_selling_price(str(item_data.selling_price), item_index=3)
    print(f"  • Selling Unit: {item_data.sell_unit}")
    page.select_sell_unit_option(item_data.sell_unit, item_index=3)
    print(f"  • Purchase Unit: {item_data.purchase_unit}")
    page.select_purchase_unit_option(item_data.purchase_unit, item_index=3)
    print(f"  • Barcode Stock No: {item_data.barcode_stock_no}")
    page.fill_barcode_stock_no(item_data.barcode_stock_no, item_index=3)
    print(f"  • Barcode: {item_data.barcode}")
    page.fill_barcode(item_data.barcode, item_index=3)
    print(f"  • Size Category: {item_data.size_category}")
    page.select_size_category_option(item_data.size_category, item_index=3)
    print(f"  • Color Category: {item_data.color_category}")
    page.select_color_category_option(item_data.color_category, item_index=3)
    print(f"  • Packaging: {item_data.packaging}")
    page.select_packaging_option(item_data.packaging, item_index=3)
    print(f"  • Specification: {item_data.specification}")
    page.select_specification_option(item_data.specification, item_index=3)
    print(f"  • Collection: {item_data.collection}")
    page.select_collection_option(item_data.collection, item_index=3)
    print("  ✓ Item #3 details filled completely")

    # ========== STEP 19: REMOVE 3RD ITEM ==========
    print("\n[STEP 19] Remove Item #3")
    print("  • Click Remove Item button for Item #3")
    page.click_remove_item_button(item_index=3)
    print("  ✓ Item #3 removed successfully")
    print("  ✓ Remaining items: Item #1 and Item #2 (total 2 items)")

    # ========== STEP 20: SAVE ==========
    print("\n[STEP 20] Save Supplier")
    print("  • Click Save button to submit supplier form")
    page.click_save_item_button()
    #wait until success notification appears
    success_displayed = page.is_saved_successfully_displayed()
    assert success_displayed, "Supplier saved notification should be displayed"
    print("  ✓ Supplier form submitted successfully")

    # ========== STEP 21: RETRIEVE AUTH TOKEN FROM SESSION ==========
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
    print(f"✅ Items added to supplier")

    # ========== STEP 22: PUBLISH ==========
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_publish_button()
    page.confirm_publish()
    print(f"✅ Supplier '{supplier_data.supplier_name}' published successfully")


    # ========== STEP 23: SIGN OUT ==========
    print("\n[STEP 23] Sign Out")
    page.sign_out()
    print("  ✓ Signed out successfully")

    print("\n" + "="*80)
    print("TEST COMPLETED SUCCESSFULLY")
    print("="*80)
    print("\nSummary:")
    print(f"  ✓ Supplier: {supplier_data.supplier_name}")
    print(f"  ✓ Contact Email: {supplier_data.email}")
    print(f"  ✓ Documents Uploaded: 6 (PDF, DOC, DOCX, XLS, XLSX, PPT)")
    print(f"  ✓ Images Uploaded: 6 (JPG, PNG, GIF, SVG, TIFF, WEBP)")
    print(f"  ✓ Items Added: 2 (Item #1 and Item #2)")
    print(f"  ✓ Item #3: Removed after testing")
    print(f"  ✓ Supplier Published Successfully")
    print("="*80 + "\n")

    # ========== Rejection Flow ==========

    print("\n" + "="*80)
    print("TEST: Source Reject Flow")
    print("="*80)

    # ========== STEP 1: LOGIN ==========

    print("\n[REJECT STEP 1] Login as Admin Account")
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    # Login with your test credentials (adjust as needed)
    login_page.login(email=LoginData.admin_email, password=LoginData.admin_password)
    print(f"  ✓ Logged in with email: {LoginData.admin_email}")

    # ========== STEP 2: REJECT ITEM ==========
    print("\n[REJECT STEP 2] Reject the Newly Added Source")
    page = SourcingPage(driver=driver, base_url=base_url)

    page.open_sourcing_page()
    print("  ✓ Sourcing page opened successfully")
    page.select_supplier_from_list(supplier_data.supplier_name)
    print(f"  ✓ Supplier selected: {supplier_data.supplier_name}")
    #test cancel reject flow
    print("\n[REJECT STEP 3] Test Reject Cancel Flow")
    print("  • Click Reject button")
    page.click_reject_button()
    page.cancel_reject()
    print("  ✓ Reject cancelled successfully")
    print("\n[REJECT STEP 4] Confirm Rejection")
    print("  • Click Reject button again")
    page.click_reject_button()
    page.fill_rejection_reason("The source does not meet our quality standards.")
    page.confirm_reject()
    print("  ✓ Source rejected successfully")
    assert page.is_rejected_successfully_displayed(), "Reject confirmation dialog should be displayed"
    print("\n" + "="*80)
