# Python Selenium Automation Framework (PyTest + POM)

OVERVIEW
--------
This project is a **beginner-friendly** Selenium automation framework
using **Python**, **PyTest**, and the **Page Object Model (POM)** pattern.

It is designed specifically for:
- Form filling
- Result assertions
- Clean, scalable, and maintainable test code


PROJECT STRUCTURE
-----------------
automation/
  tests/
    test_template.py      # Example test using POM and fixtures
    conftest.py           # Shared PyTest fixtures (WebDriver, base URL, etc.)
  pages/
    base_page.py          # Base class for all pages (shared helpers)
    page_template.py      # Example Page Object for a form
  locators/
    locators_template.py  # Example locators for the form page
  data/
    data_template.py      # Example test data for the form
  config/
    settings.py           # Global configuration (URL, timeout, browser)
  requirements.txt        # Python dependencies (pytest, selenium)
  README.md               # This file


HOW THE FRAMEWORK WORKS
-----------------------
The framework follows the **Page Object Model (POM)** and **explicit waits only**:

- **Tests (`tests/`)**
  - Contain **test logic and assertions only**.
  - Use fixtures (e.g., `driver`, `base_url`) from `conftest.py`.
  - Call methods on Page Objects to interact with the UI.

- **Pages (`pages/`)**
  - Each page class represents a screen or page in your application.
  - Inherit from `BasePage` in `base_page.py`.
  - Contain **UI actions and getters only** (no assertions).

- **Locators (`locators/`)**
  - Store all Selenium `By.*` locator tuples.
  - Keep selectors separate from page logic and tests.

- **Data (`data/`)**
  - Store test input values and expected values.
  - Keep data separate from locators, pages, and tests.

- **Config (`config/settings.py`)**
  - Central place for:
    - `BASE_URL` (target application URL)
    - `EXPLICIT_WAIT_TIMEOUT` (in seconds)
    - `BROWSER` (default: `"chrome"`)

- **WebDriver Lifecycle (`tests/conftest.py`)**
  - Uses PyTest fixtures to:
    - **Initialize** WebDriver before each test.
    - **Quit** WebDriver after each test.
  - Tests **must not** create WebDriver instances directly.


SETUP AND INSTALLATION
----------------------
**Step 1: Create a Virtual Environment (venv)**
   - Navigate to the `automation/` folder (this folder where you're reading the README).
   - Create a virtual environment:
     ```
     python -m venv .venv
     ```
   - This creates a `.venv/` folder inside the `automation/` folder.
   - **Why inside automation/?** This keeps everything automation-related
     self-contained in one place, making it easier to manage and delete if needed.

**Step 2: Activate the Virtual Environment**
   - Make sure you're in the `automation/` folder (where `.venv/` was created).
   - **Windows (PowerShell):**
     ```
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```
     .venv\Scripts\activate.bat
     ```
   - **Linux/Mac:**
     ```
     source .venv/bin/activate
     ```
   - You should see `(.venv)` in your terminal prompt when activated.

**Step 3: Install Dependencies**
   - While still in the `automation/` folder (with venv activated), install
     all required packages from `requirements.txt`:
     ```
     pip install -r requirements.txt
     ```
   - This installs PyTest and Selenium with the specified versions.

**Note:** Both `requirements.txt` and `.venv/` are located inside `automation/`
   folder to keep all automation-related files and dependencies self-contained.


CONFIGURING THE FRAMEWORK
-------------------------
1. Open `config/settings.py`.
2. Update the following values:
   - `BASE_URL`               # Your application's base URL
   - `EXPLICIT_WAIT_TIMEOUT`  # Default explicit wait timeout (e.g., 10)
   - `BROWSER`                # Currently supports: "chrome"

Example:
    BASE_URL = "https://your-app-under-test.com"
    EXPLICIT_WAIT_TIMEOUT = 15
    BROWSER = "chrome"


HOW TO CREATE A NEW TEST (STEP-BY-STEP)
---------------------------------------
This section walks you through creating a new POM-style test
using the provided templates.

STEP 1: CREATE/UPDATE LOCATORS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Open `locators/locators_template.py`.
2. In the "UPDATE LOCATORS BELOW" section:
   - Replace `ExampleFormLocators` with locators matching your page,
     or create a new class (e.g., `LoginPageLocators`).
3. Use appropriate Selenium `By.*` strategies:
   - `By.ID`, `By.NAME`, `By.CSS_SELECTOR`, `By.XPATH`, etc.

Example (new locator class):
    class LoginPageLocators:
        USERNAME_INPUT = (By.ID, "username")
        PASSWORD_INPUT = (By.ID, "password")
        LOGIN_BUTTON = (By.ID, "login")


STEP 2: CREATE A PAGE OBJECT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Copy `pages/page_template.py` and rename it, e.g.:
   - `pages/login_page.py`
2. Open the new file and:
   - Rename the class (e.g., `LoginPage`).
   - Update the locator import to use your new locator class
     (e.g., `LoginPageLocators`).
   - Implement methods that:
     - Perform actions (e.g., `enter_username`, `click_login`).
     - Return information used for assertions (e.g., `is_error_visible`).
3. Keep the class focused on UI interactions and getters ONLY.
   - No assertions, no test logic.


STEP 3: DEFINE TEST DATA
~~~~~~~~~~~~~~~~~~~~~~~~
1. Open `data/data_template.py`.
2. Either:
   - Update `ExampleFormData`, or
   - Create a new data class (e.g., `LoginData`) using `@dataclass`.
3. Store:
   - Input values (usernames, passwords, messages).
   - Expected texts/messages (success or error messages).

Example:
    @dataclass(frozen=True)
    class LoginData:
        valid_username: str = "test_user"
        valid_password: str = "secure_password"
        expected_welcome_text: str = "Welcome, test_user!"


STEP 4: WRITE A NEW TEST
~~~~~~~~~~~~~~~~~~~~~~~~
1. Open `tests/test_template.py`.
2. Use it as a reference and create a new test file, such as:
   - `tests/test_login.py`
3. In your new test file:
   - Import your Page Object and data class.
   - Use PyTest fixtures (`driver`, `base_url`) by adding them
     as function parameters.
   - Write the test so it **reads like English**:
     - GIVEN the user is on the Login page
     - WHEN they enter valid credentials and submit
     - THEN they should see a welcome message

Example structure:
    def test_user_can_log_in_with_valid_credentials(driver, base_url):
        page = LoginPage(driver=driver, base_url=base_url)
        data = LoginData()

        page.open_login_page()
        page.enter_username(data.valid_username)
        page.enter_password(data.valid_password)
        page.click_login()

        assert page.is_welcome_message_visible()
        assert data.expected_welcome_text in page.get_welcome_message_text()


WHERE TO UPDATE LOCATORS AND DATA
---------------------------------
- **Locators**
  - File: `locators/locators_template.py` (and any new locator files you add).
  - Section: Look for comments like `UPDATE LOCATORS BELOW`.
  - Responsibility: Keep selectors accurate as the UI changes.

- **Data**
  - File: `data/data_template.py` (and any new data files you add).
  - Section: Look for comments like `INPUT TEST DATA HERE`.
  - Responsibility: Keep test values and expectations up to date.


RUNNING THE TESTS
-----------------
1. Make sure your virtual environment is activated (see SETUP above).
   - You should be in the `automation/` folder with `(.venv)` in your prompt.

2. Run the tests:
   ```
   pytest tests -v
   ```
   Or, if you're running from the project root:
   ```
   pytest selenium automation/tests -v
   ```

3. PyTest will:
   - Discover tests in `automation/tests/`.
   - Use fixtures from `conftest.py` to manage WebDriver.
   - Run your tests and display results.


KEY RULES (SUMMARY)
-------------------
- **DO NOT** create WebDriver instances in test files.
  - Always use the `driver` fixture from `conftest.py`.
- **DO NOT** write assertions in Page Objects.
  - Keep them in test files only.
- **DO** keep locators and data in their dedicated modules.
  - `locators/` for selectors.
  - `data/` for input values and expected results.
- **DO** use explicit waits only.
  - Rely on helper methods in `BasePage` (`wait_for_visible`, etc.).


