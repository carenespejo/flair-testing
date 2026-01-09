"""
============================================================
 sourcing_page.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- Defines the SourcingPage class that extends BasePage.
- Contains page-specific methods for interacting with the Sourcing page.
- Uses locators from sourcing_locators.py.

WHAT YOU SHOULD EDIT
--------------------
- Add new page-specific methods for the Sourcing page here.
"""

from __future__ import annotations

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from locators.sourcing_locators import SourcingPageLocators


class SourcingPage(BasePage):
    """
    Page Object for the Sourcing page.
    """

    def _get_item_locator(self, base_locator: tuple, item_index: int = None) -> tuple:
        """
        Get a locator adjusted for a specific item index.
        When item_index is provided, wraps the locator to target that specific item's element.
        Converts ID-based locators to XPath to support position indexing.
        
        Args:
            base_locator: A tuple of (By, locator_string) for the base element
            item_index: Optional 1-based item index to target a specific item
        
        Returns:
            Adjusted locator tuple, or original if item_index is None
        """
        if not item_index:
            return base_locator
        
        by_type, locator_str = base_locator

        # Scope the locator to the specific item card instead of relying on global ordering.
        # This is more robust when the same IDs repeat inside each item block.
        item_container_xpath = SourcingPageLocators.ITEMS_CONTAINER[1]

        if by_type == By.ID:
            # Locate the element by id within the Nth item container
            adjusted_xpath = f"({item_container_xpath})[{item_index}]//*[@id='{locator_str}']"
            return (By.XPATH, adjusted_xpath)
        elif by_type == By.XPATH:
            # If the provided locator is an absolute XPath (starts with '/'), append it as a descendant
            if locator_str.startswith('/'):
                adjusted_xpath = f"({item_container_xpath})[{item_index}]{locator_str}"
            else:
                adjusted_xpath = f"({item_container_xpath})[{item_index}]//{locator_str}"
            return (By.XPATH, adjusted_xpath)
        else:
            return base_locator

    def open_sourcing_page(self) -> None:
        """Navigate to the Sourcing page URL."""
        self.open("/sourcing")

    def click_new_source_button(self) -> None:
        """Click the 'New Source' button."""
        self.click(SourcingPageLocators.NEW_SOURCE_BUTTON)

    def fill_supplier_name(self, name: str) -> None:
        """Fill supplier name in the input field."""
        self.type_text(SourcingPageLocators.SUPPLIER_NAME_INPUT, name)

    def fill_supplier_address(self, address: str) -> None:
        """Fill supplier address in the input field."""
        self.type_text(SourcingPageLocators.SUPPLIER_ADDRESS_INPUT, address)

    def fill_contact_person(self, person: str) -> None:
        """Fill contact person name in the input field."""
        self.type_text(SourcingPageLocators.CONTACT_PERSON_INPUT, person)

    def fill_contact_address(self, address: str) -> None:
        """Fill contact address in the input field."""
        self.type_text(SourcingPageLocators.CONTACT_ADDRESS_INPUT, address)

    def fill_contact_number(self, number: str) -> None:
        """Fill contact number in the input field."""
        self.type_text(SourcingPageLocators.CONTACT_NUMBER_INPUT, number)

    def fill_email(self, email: str) -> None:
        """Fill email in the input field."""
        self.type_text(SourcingPageLocators.EMAIL_INPUT, email)

    def add_attachment(self, file_path: str) -> None:
        """Add an attachment by uploading a file."""
        self.upload_file(SourcingPageLocators.ATTACHMENT_INPUT, file_path)

    def add_multiple_attachments(self, file_paths_string: str) -> None:
        """
        Add multiple attachments by uploading multiple files at once.
        
        This method sends file paths to the hidden input element.
        The file input will process the paths and upload them.
        
        Args:
            file_paths_string: Newline-separated string of full file paths.
                              Example: "C:\\path\\to\\file1.pdf\\nC:\\path\\to\\file2.docx"
        """
        import time
        
        # Find the hidden file input element
            # Find the hidden file input element and send the file paths
        file_input = self.driver.find_element(By.ID, "supplier-files")
        file_input.send_keys(file_paths_string)

        # Wait until the attachments container is present (files processing begins)
        try:
            self.wait.until(EC.presence_of_element_located(SourcingPageLocators.ATTACHMENTS_CONTAINER))
        except Exception:
            # fallback small sleep if wait fails for any reason
            import time
            time.sleep(1)

    def fill_item_name(self, name: str, item_index: int = None) -> None:
        """
        Fill item name in the input field.
        
        Args:
            name: The item name to fill.
            item_index: Optional item index (1-based). If provided, targets that specific item.
        """
        locator = self._get_item_locator(SourcingPageLocators.ITEM_NAME_INPUT, item_index)
        self.type_text(locator, name)

    def fill_item_description(self, description: str, item_index: int = None) -> None:
        """
        Fill item description in the input field.
        
        Args:
            description: The item description to fill.
            item_index: Optional item index (1-based). If provided, targets that specific item.
        """
        locator = self._get_item_locator(SourcingPageLocators.ITEM_DESCRIPTION_INPUT, item_index)
        self.type_text(locator, description)

    def select_brand_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific brand option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.BRAND_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.BRAND_OPTION[1], option_name)

    def select_department_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific department option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.DEPARTMENT_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.DEPARTMENT_OPTION[1], option_name)

    def select_sub_department_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific sub-department option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.SUB_DEPARTMENT_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.SUB_DEPARTMENT_OPTION[1], option_name)

    def select_category_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific category option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.CATEGORY_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.CATEGORY_OPTION[1], option_name)

    def select_item_group_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific item group option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.ITEM_GROUP_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.ITEM_GROUP_OPTION[1], option_name)

    def select_style_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific style option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.STYLE_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.STYLE_OPTION[1], option_name)

    def fill_selling_price(self, price: str, item_index: int = None) -> None:
        """
        Fill item selling price in the input field.
        
        Args:
            price: The item selling price to fill.
            item_index: Optional item index (1-based). If provided, targets that specific item.
        """
        locator = self._get_item_locator(SourcingPageLocators.SELLING_PRICE, item_index)
        self.type_text(locator, price)
    
    def select_sell_unit_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific selling unit option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.SELL_UNIT_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.SELL_UNIT_OPTION[1], option_name)

    def select_purchase_unit_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific purchase unit option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.PURCHASE_UNIT_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.PURCHASE_UNIT_OPTION[1], option_name)

    def fill_barcode_stock_no(self, stock_no: str, item_index: int = None) -> None:
        """
        Fill item barcode stock number in the input field.
        
        Args:
            stock_no: The item barcode stock number to fill.
            item_index: Optional item index (1-based). If provided, targets that specific item.
        """
        locator = self._get_item_locator(SourcingPageLocators.BARCODE_STOCK_NO_INPUT, item_index)
        self.type_text(locator, stock_no)

    def fill_barcode(self, barcode: str, item_index: int = None) -> None:
        """
        Fill item barcode in the input field.
        
        Args:
            barcode: The item barcode to fill.
            item_index: Optional item index (1-based). If provided, targets that specific item.
        """
        locator = self._get_item_locator(SourcingPageLocators.BARCODE_INPUT, item_index)
        self.type_text(locator, barcode)

    def select_size_category_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific size category option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.SIZE_CATEGORY_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.SIZE_CATEGORY_OPTION[1], option_name)

    def select_color_category_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific color category option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.COLOR_CATEGORY_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.COLOR_CATEGORY_OPTION[1], option_name)

    def select_packaging_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific packaging option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.PACKAGING_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.PACKAGINGOPTION[1], option_name)

    def select_specification_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific specification option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.SPECIFICATION_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.SPECIFICATION_OPTION[1], option_name)

    def select_collection_option(self, option_name: str, item_index: int = None) -> None:
        """Select a specific collection option from the dropdown."""
        combo_locator = self._get_item_locator(SourcingPageLocators.COLLECTION_COMBO, item_index)
        super().select_dropdown(combo_locator, SourcingPageLocators.COLLECTION_OPTION[1], option_name)

    def fill_remarks(self, remarks: str) -> None:
        """Fill remarks in the input field."""
        self.type_text(SourcingPageLocators.REMARKS_INPUT, remarks)

    def click_add_item_button(self) -> None:
        """Click the '+ Add Item' button."""
        # Count items then click Add Item and wait for a new item to appear
        try:
            prev_count = self.get_item_count()
        except Exception:
            prev_count = 0

        button = self.driver.find_element(*SourcingPageLocators.ADD_ITEM_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", button)
        self.click(SourcingPageLocators.ADD_ITEM_BUTTON)

        # Wait until the item count increases (new item card appears)
        try:
            self.wait.until(lambda d: self.get_item_count() > prev_count)
        except Exception:
            # if timeout, continue; tests may handle absence
            pass

    def click_save_item_button(self) -> None:
        """Click the 'Save Item' button."""
        self.click(SourcingPageLocators.SAVE_ITEM_BUTTON)

    def click_cancel_item_button(self) -> None:
        """Click the 'Cancel' button."""
        self.click(SourcingPageLocators.CANCEL_ITEM_BUTTON)

    def select_supplier_from_list(self, supplier_name: str) -> None:
        """Select a supplier from the list by name."""
        supplier_locator = (By.XPATH, f"//li[.//span[contains(@class, 'text-sm') and normalize-space(text())='{supplier_name}']]")
        self.click(supplier_locator)

    def wait_for_attachments(self, expected_count: int, timeout: int = 10) -> None:
        """
        Wait for expected number of attachments to be displayed in the attachments container.
        
        Args:
            expected_count: The expected number of attachments to wait for.
            timeout: Maximum time to wait in seconds (default: 10).
        """
        import time as time_module
        
        start_time = time_module.time()
        
        while time_module.time() - start_time < timeout:
            try:
                attachments_container = self.driver.find_element(
                    *SourcingPageLocators.ATTACHMENTS_CONTAINER
                )
                
                elements = attachments_container.find_elements(
                    By.XPATH, ".//div[contains(@class,'font-medium')]"
                )
                
                if len(elements) >= expected_count:
                    return
                    
            except Exception as e:
                print(f"Waiting for attachments container... ({time_module.time() - start_time:.1f}s)")
            
            time_module.sleep(0.5)
        
        raise TimeoutException(
            f"Expected {expected_count} attachments but container not found or timeout reached"
        )

    def get_displayed_attachment_names(self) -> list:
        """
        Get all displayed attachment file names from the attachments container.
        
        Returns:
            List of attachment file names currently displayed.
        """
        container = self.driver.find_element(*SourcingPageLocators.ATTACHMENTS_CONTAINER)

        return [
            el.text.strip()
            for el in container.find_elements(
                By.XPATH, ".//div[contains(@class,'font-medium')]"
            )
        ]

    def get_total_attachment_count(self) -> int:
        """
        Get the total count of all attachments (documents and images combined).
        
        Returns:
            Total number of attachment items in the container.
        """
        try:
            container = self.driver.find_element(*SourcingPageLocators.ATTACHMENTS_CONTAINER)
            # Count all child divs with the attachment item classes
            attachment_items = container.find_elements(
                By.XPATH, ".//div[contains(@class, 'w-24') or contains(@class, 'w-28')]"
            )
            return len(attachment_items)
        except Exception:
            return 0

    def get_image_attachment_count(self) -> int:
        """
        Get the count of image attachments in the container.
        
        Returns:
            Number of image elements in the attachments container.
        """
        try:
            container = self.driver.find_element(*SourcingPageLocators.ATTACHMENTS_CONTAINER)
            # Count img elements (images are rendered as img tags)
            image_elements = container.find_elements(By.XPATH, ".//img")
            return len(image_elements)
        except Exception:
            return 0

    def is_attachment_displayed(self, file_name: str) -> bool:
        """
        Check if an attachment with the given file name is displayed in the attachments container.
        
        Args:
            file_name: The name of the file to check for.
        
        Returns:
            True if the attachment is displayed, False otherwise.
        """
        try:
            self.wait_for_attachments(expected_count=1)
            displayed_files = self.get_displayed_attachment_names()
            return file_name in displayed_files
        except Exception:
            return False

    def are_all_attachments_displayed(self, file_names: list) -> bool:
        """
        Check if all attachments with the given file names are displayed.
        
        Args:
            file_names: List of file names to check for.
        
        Returns:
            True if all attachments are displayed, False otherwise.
        """
        self.wait_for_attachments(expected_count=len(file_names))

        displayed_files = self.get_displayed_attachment_names()

        missing_files = set(file_names) - set(displayed_files)

        if missing_files:
            print(f"Missing attachments: {missing_files}")
            print(f"Displayed attachments: {displayed_files}")
            return False

        return True

    def invalid_email_displayed(self) -> bool:
        """Check if invalid email notification is displayed."""
        return self.is_visible(SourcingPageLocators.INVALID_EMAIL)
    
    def no_item_displayed(self) -> bool:
        """Check if no item notification is displayed."""
        return self.is_visible(SourcingPageLocators.NO_ITEM)
    
    def rejected_files_displayed(self) -> bool:
        """Check if rejected files notification is displayed."""
        return self.is_visible(SourcingPageLocators.REJECTED_FILES)
    
    def email_required_displayed(self) -> bool:
        """Check if required contact email notification is displayed."""
        return self.is_visible(SourcingPageLocators.REQUIRED_CONTACT_EMAIL)

    def supplier_name_required_displayed(self) -> bool:
        """Check if required supplier name notification is displayed."""
        return self.is_visible(SourcingPageLocators.REQUIRED_SUPPLIER_NAME)
    
    def is_saved_successfully_displayed(self) -> bool:
        """Check if saved successfully notification is displayed."""

        return self._wait_for_visible(SourcingPageLocators.SAVED_SUCCESSFULLY) is not None
    
    def item_product_name_required_displayed(self, item_index: int) -> bool:
        """
        Check if product name required validation error is displayed for a specific item.
        
        Args:
            item_index: The index of the item (1-based, e.g., 1 for Item #1, 2 for Item #2).
        
        Returns:
            True if the validation error is displayed for the specified item, False otherwise.
        """
        # Format the locator for the product-name-required message with the item index
        locator_xpath = SourcingPageLocators.ITEM_PRODUCT_NAME_REQUIRED[1].format(item_index=item_index)
        locator = (By.XPATH, locator_xpath)
        return self.is_visible(locator)
    
    def click_remove_item_button(self, item_index: int) -> None:
        """
        Click the 'Remove Item' button for a specific item by index.
        
        Args:
            item_index: The index of the item to remove (1-based, e.g., 1 for first item, 2 for second)
        """
        locator_xpath = SourcingPageLocators.REMOVE_ITEM_BUTTON[1].format(item_index=item_index)
        locator = (By.XPATH, locator_xpath)
        # Scroll into view to avoid sticky header interception, then click
        try:
            el = self._wait_for_visible(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", el)
        except Exception:
            pass
        self.click(locator)

    def get_item_count(self) -> int:
        items = self.driver.find_elements(*SourcingPageLocators.ITEMS_CONTAINER)
        return len(items)
    
    def click_item_card_by_name(self, item_name: str) -> None:
        """
        Click the item card by item name.
        
        Args:
            item_name: The name of the item to click.
        """
        item_locator = (By.XPATH, SourcingPageLocators.ITEM_CARD_BY_NAME[1].format(item_name=item_name))
        self.click(item_locator)

    def click_edit_item_button_by_name(self, item_name: str) -> None:
        """
        Click the edit item button by item name.
        
        Args:
            item_name: The name of the item to edit.
        """
        edit_button_locator = (By.XPATH, SourcingPageLocators.EDIT_ITEM_BUTTON_BY_NAME[1].format(item_name=item_name))
        self.click(edit_button_locator)

    def click_delete_item_button_by_name(self, item_name: str) -> None:
        """
        Click the delete item button by item name.
        Then confirm the deletion in the alert dialog.
        
        Args:
            item_name: The name of the item to delete.
        """
        delete_button_locator = (By.XPATH, SourcingPageLocators.DELETE_ITEM_BUTTON_BY_NAME[1].format(item_name=item_name))
        self.click(delete_button_locator)
        alert = self.driver.switch_to.alert
        alert.accept()

    def click_update_item_button(self) -> None:
        """Click the 'Update Item' button."""
        self.click(SourcingPageLocators.UPDATE_ITEM_BUTTON)

    def get_item_name_input_value(self) -> str:
        """
        Get the current value of the item name input field.
        
        Args:
            item_index: Optional item index (1-based). If provided, targets that specific item.
        
        Returns:
            The current value of the item name input field as a string.
        """
        return self.get_field_value(SourcingPageLocators.ITEM_NAME_INPUT)
    
    def click_publish_button(self) -> None:
        """Click the 'Publish' button."""
            # I need to fix this: FAILED tests/Sourcing Page/test_publish.py::test_publish_item_successfully - selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <button type="button" class="px-3 py-2 bg-primary text-white rounded-lg text-sm disabl...
        self.click(SourcingPageLocators.PUBLISH_BUTTON)

    def confirm_publish(self) -> None:
        """Click the 'Confirm' button in the publish confirmation dialog."""
        self.click(SourcingPageLocators.MODAL_CONFIRM_BUTTON)

    def cancel_publish(self) -> None:
        """Click the 'Cancel' button in the publish confirmation dialog."""
        self.click(SourcingPageLocators.MODAL_CANCEL_BUTTON)

    def is_published_successfully_displayed(self) -> bool:
        """Check if published successfully notification is displayed."""
        return self._wait_for_visible(SourcingPageLocators.PUBLISHED_SUCCESSFULLY) is not None
    
    #ADMIN CLERK ACCOUNT METHODS
    def click_approve_button(self) -> None:
        """Click the 'Approve' button."""
        self.click(SourcingPageLocators.APPROVE_BUTTON)

    def confirm_approve(self) -> None:
        """Click the 'Confirm' button in the approve confirmation dialog."""
        self.click(SourcingPageLocators.MODAL_CONFIRM_BUTTON)

    def cancel_approve(self) -> None:
        """Click the 'Cancel' button in the approve confirmation dialog."""
        self.click(SourcingPageLocators.MODAL_CANCEL_BUTTON)

    def click_reject_button(self) -> None:
        """Click the 'Reject' button."""
        self.click(SourcingPageLocators.REJECT_BUTTON)
    
    def cancel_reject(self) -> None:
        """Click the 'Cancel' button in the reject confirmation dialog."""
        self.click(SourcingPageLocators.CANCEL_REJECT_BUTTON)

    def fill_rejection_reason(self, reason: str) -> None:
        """Fill rejection reason in the input field."""
        self.type_text(SourcingPageLocators.REJECTION_REASON_INPUT, reason)

    def confirm_reject(self) -> None:
        """Click the 'Confirm Reject' button in the reject confirmation dialog."""
        self.click(SourcingPageLocators.CONFIRM_REJECT_BUTTON)

    def is_approved_successfully_displayed(self) -> bool:
        """Check if approved successfully notification is displayed."""
        return self._wait_for_visible(SourcingPageLocators.APPROVED_SUCCESSFULLY) is not None
    
    def is_rejected_successfully_displayed(self) -> bool:
        """Check if rejected successfully notification is displayed."""
        return self._wait_for_visible(SourcingPageLocators.REJECTED_SUCCESSFULLY) is not None
    
    def sign_out(self) -> None:
        """Click the 'Sign out' button to log out."""
        self.click(SourcingPageLocators.SIGN_OUT_BUTTON)