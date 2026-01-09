from __future__ import annotations

import requests
from pages.sourcing_page import SourcingPage
from pages.login_page import LoginPage
from data.source_data import supplier1, item1, supplier2
from data.api_helper import ItemSourcingAPI
from data.login_data import LoginData
#import the timer sleep
from time import sleep

def test_approve_item_successfully(driver, base_url):
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
    login_page.login(email=LoginData.admin_email, password=LoginData.admin_password)

    # ========== STEP 2: FILL AND SUBMIT SOURCING FORM ==========
    page = SourcingPage(driver=driver, base_url=base_url)
    supplier_data = supplier1

    page.open_sourcing_page()
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_approve_button()
    page.cancel_approve()
    page.click_approve_button()
    page.confirm_approve()

    assert page.is_approved_successfully_displayed(), "Approve confirmation dialog should be displayed"

def test_reject_item_successfully(driver, base_url):
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
    login_page.login(email=LoginData.admin_email, password=LoginData.admin_password)

    # ========== STEP 2: FILL AND SUBMIT SOURCING FORM ==========
    page = SourcingPage(driver=driver, base_url=base_url)
    data = item1
    supplier_data = supplier2

    page.open_sourcing_page()
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_reject_button()
    page.cancel_reject()
    page.click_reject_button()
    page.fill_rejection_reason("Automated rejection for testing purposes.")
    page.confirm_reject()
    
    assert page.is_rejected_successfully_displayed(), "Reject confirmation dialog should be displayed"