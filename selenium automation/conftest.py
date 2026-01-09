"""
============================================================
 conftest.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- Central place for PyTest fixtures shared across all tests.
- Responsible for:
  - INITIALIZING the Selenium WebDriver before each test.
  - TEARING DOWN (quitting) the WebDriver after each test.
  - Providing configuration fixtures like `base_url`.

WHAT YOU SHOULD EDIT
--------------------
- You MAY:
  - Add new fixtures (e.g., page object factories).
  - Adjust the WebDriver options (headless mode, window size, etc.).

WHAT YOU SHOULD NOT EDIT
------------------------
- DO NOT INITIALIZE WEBDRIVER INSIDE INDIVIDUAL TEST FILES.
  - Always use the `driver` fixture defined here.
- DO NOT REMOVE THE `driver` OR `base_url` FIXTURES.
"""

from __future__ import annotations

import os
import logging
import pytest
import webbrowser
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.settings import (
    DEFAULT_BASE_URL,
    DEFAULT_BROWSER,
    DEFAULT_HEADLESS,
)

# ============================================================
# INTERNAL HELPERS (DO NOT MODIFY UNLESS NECESSARY)
# ============================================================

# Global variable to store the report path for opening after tests
_report_path = None

DEFAULT_DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")  # you can change this

def _create_chrome_driver() -> webdriver.Chrome:
    """
    Create and configure a Chrome WebDriver instance with automatic downloads.
    """
    options = ChromeOptions()

    # Headless mode if desired
    if DEFAULT_HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    # -----------------------------
    # Chrome preferences for download
    # -----------------------------
    prefs = {
        "download.default_directory": DEFAULT_DOWNLOAD_DIR,
        "download.prompt_for_download": False,   # bypass 'Save As' dialog
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Ensure the download directory exists
    os.makedirs(DEFAULT_DOWNLOAD_DIR, exist_ok=True)

    return driver


# ============================================================
# PYTEST FIXTURES
# ============================================================


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Base URL fixture.

    - Tests should use this instead of hardcoding URLs.
    - Value is configured in `config/settings.py`.
    """
    return DEFAULT_BASE_URL


@pytest.fixture(scope="function")
def driver() -> webdriver.Remote:
    """
    WebDriver fixture.

    - Initializes the WebDriver BEFORE each test function.
    - Quits the WebDriver AFTER each test function.
    - Uses Chrome as the default browser (configurable).

    IMPORTANT:
    - DO NOT INITIALIZE WEBDRIVER INSIDE TEST FILES.
      Always depend on this fixture instead:

      def test_example(driver):
          driver.get("https://example.com")
    """
    if DEFAULT_BROWSER.lower() != "chrome":
        raise ValueError(
            f"Only 'chrome' browser is supported in this template. "
            f"Configured value: {DEFAULT_BROWSER}"
        )

    driver_instance = _create_chrome_driver()
    try:
        yield driver_instance
    finally:
        driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshot if a test fails with incrementing filename.
    """
    outcome = yield
    rep = outcome.get_result()
    # Only act on the call phase (test function execution)
    if rep.when == "call":
        driver = item.funcargs.get("driver")
        if not driver:
            return

        screenshot_folder = "screenshots"
        os.makedirs(screenshot_folder, exist_ok=True)

        # Create incrementing filename with timestamp and status
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        counter = 1
        status = "failed" if rep.failed else ("passed" if rep.passed else "other")

        while True:
            filename = f"{item.name}_{status}_{timestamp}_{counter:03d}.png"
            filepath = os.path.join(screenshot_folder, filename)
            if not os.path.exists(filepath):
                break
            counter += 1

        try:
            driver.save_screenshot(filepath)
            if rep.failed:
                logging.error(f"Test failed. Screenshot saved to {filepath}")
            elif rep.passed:
                logging.info(f"Test passed. Screenshot saved to {filepath}")
        except Exception:
            logging.exception("Failed to save screenshot for test '%s'", item.name)


def _get_next_report_filename() -> str:
    """
    Generate an incrementing report filename with timestamp.
    
    Returns:
        str: Filename like "report_20251216_143022_001.html"
    """
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    counter = 1
    
    while True:
        filename = f"report_{timestamp}_{counter:03d}.html"
        filepath = reports_dir / filename
        if not filepath.exists():
            return filename
        counter += 1


def pytest_configure(config):
    """
    PyTest hook to set the HTML report filename before tests run.
    Ensures each test run gets a unique incrementing report name.
    """
    global _report_path
    report_filename = _get_next_report_filename()
    report_path = f"reports/{report_filename}"
    _report_path = report_path
    
    # Add the HTML report option dynamically
    config.option.htmlpath = report_path


def pytest_sessionfinish(session, exitstatus):
    """
    PyTest hook that runs after all tests are complete.
    Opens the generated HTML report in the default browser.
    """
    global _report_path
    if _report_path and Path(_report_path).exists():
        report_url = Path(_report_path).resolve().as_uri()
        webbrowser.open(report_url)
        logging.info(f"Opening HTML report: {report_url}")

