
from selenium.webdriver.common.by import By

# ============================================================
# UPDATE LOCATORS BELOW
# ============================================================


class DashboardPageLocators:
    """
    Locators for the Example Form page.

    - Replace these locators with real ones from your application.
    - This file is safe to copy and adapt for new pages.
    """

    # TODO: UPDATE THESE SELECTORS TO MATCH YOUR REAL APPLICATION
    USER_ROLE = (By.XPATH, '//*[@id="app"]/div/div/div[2]/header/div[2]/div[2]/div[2]/span')
    SIGN_OUT_BUTTON = (By.XPATH, '//*[@id="app"]/div/div/div/header/div[2]/div[2]/button')
