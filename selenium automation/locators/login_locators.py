from selenium.webdriver.common.by import By


# ============================================================
# UPDATE LOCATORS BELOW
# ============================================================


class LoginPageLocators:
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")