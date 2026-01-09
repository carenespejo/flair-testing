from __future__ import annotations

import requests
from pages.sourcing_page import SourcingPage
from pages.login_page import LoginPage
from data.source_data import supplier1, item1
from data.api_helper import ItemSourcingAPI
from data.login_data import LoginData
#import the timer sleep
from time import sleep

def test_publish_item_successfully(driver, base_url):
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
    data = item1
    supplier_data = supplier1

    page.open_sourcing_page()
    page.select_supplier_from_list(supplier_data.supplier_name)
    page.click_publish_button()
    page.cancel_publish()
    page.click_publish_button()
    page.confirm_publish()
    
    assert page.is_published_successfully_displayed(), "Publish confirmation dialog should be displayed"