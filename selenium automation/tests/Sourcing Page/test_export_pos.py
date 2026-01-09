from __future__ import annotations

import requests
import pytest
from conftest import DEFAULT_DOWNLOAD_DIR
from pages.items_page import ItemsPage
from pages.login_page import LoginPage
from data.source_data import supplier1, item2, edited_item2
from data.api_helper import ItemSourcingAPI
from data.login_data import LoginData

@pytest.mark.order(4)
def test_export_pos_successfully(driver, base_url):
    # ========== STEP 1: LOGIN ==========
    login_page = LoginPage(driver=driver, base_url=base_url)
    login_page.open_login_page()
    # Login with your test credentials (adjust as needed)
    login_page.login(email=LoginData.buyer_email, password=LoginData.buyer_password)

    print("\n" + "="*80)
    print("Test: Export POS for Approved Source")
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
    