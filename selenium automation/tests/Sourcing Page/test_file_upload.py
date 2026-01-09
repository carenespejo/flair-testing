from __future__ import annotations

import requests
from pages.sourcing_page import SourcingPage
from pages.login_page import LoginPage
from data.source_data import supplier1, item1
from data.api_helper import ItemSourcingAPI
from data.login_data import LoginData
from data.files_data import *


def test_valid_documents_successfully(driver, base_url):
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
    
    # Upload multiple files at once using the page method
    file_paths = get_valid_document_paths()
    page.add_multiple_attachments(file_paths)

    # Check all attachments are displayed
    file_names = ["TEST_PDF.pdf", "TEST_DOC.doc", "TEST_DOCX.docx", "TEST_XLS.xls", "TEST_XLSX.xlsx", "TEST_PPT.ppt"]
    assert page.are_all_attachments_displayed(file_names), "Not all attachments were uploaded successfully."

def test_invalid_file_upload(driver, base_url):
    """
    GIVEN the user logs in to the application
    WHEN the user navigates to Sourcing and attempts to upload invalid file types
    THEN appropriate error messages should be displayed.
    """

    # ========== STEP 1: LOGIN ==========
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    # Login with your test credentials (adjust as needed)
    login_page.login(email=LoginData.buyer_email, password=LoginData.buyer_password)

    # ========== STEP 2: ATTEMPT TO UPLOAD INVALID FILES ==========
    page = SourcingPage(driver=driver, base_url=base_url)
    page.open_sourcing_page()
    page.click_new_source_button()

    # Attempt to upload invalid files
    invalid_files = [
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_EXE.exe",
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_BAT.bat",
        "D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\INVALID FILES\\TEST_SH.sh",
    ]
    
    page.add_multiple_attachments("\n".join(invalid_files))
    
    # Assert that rejected files notification is displayed
    assert page.rejected_files_displayed(), "Rejected files notification was not displayed for invalid file types."