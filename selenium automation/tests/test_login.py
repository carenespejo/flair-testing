from __future__ import annotations

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from data.login_data import LoginData

@pytest.mark.order(1)
def test_buyer_login(driver, base_url):
    """Buyer can log in and reach dashboard."""
    login_page = LoginPage(driver,base_url)
    credentials = LoginData()

    login_page.open_login_page()
    login_page.login(credentials.buyer_email, credentials.buyer_password)
    dashboard = DashboardPage(driver, base_url)
    dashboard.open_dashboard_page()

    assert dashboard.check_login_status(), "Login failed with valid buyer credentials."
    print("Buyer login test passed successfully:")
    print("✅Able to login as Buyer and reach dashboard.")

@pytest.mark.order(2)
def test_admin_login(driver, base_url):
    """Admin can log in and reach dashboard."""
    login_page = LoginPage(driver, base_url)
    credentials = LoginData()

    login_page.open_login_page()
    login_page.login(credentials.admin_email, credentials.admin_password)
    dashboard = DashboardPage(driver,base_url)
    dashboard.open_dashboard_page()

    assert dashboard.check_login_status(), "Login failed with valid admin credentials."
    print("Admin login test passed successfully.")
    print("✅Able to login as Admin and reach dashboard.")