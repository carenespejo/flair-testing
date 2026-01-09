from __future__ import annotations

import glob
import os
import time
from pages.base_page import BasePage
from locators.items_locators import ItemsPageLocators

class ItemsPage(BasePage):
    def open_items_page(self) -> None:
        self.open("/items")

    def select_supplier(self, supplier_name: str) -> None:
        """Select a supplier from the list by name."""
        locator = (ItemsPageLocators.SELECTED_SUPPLIER[0],
                   ItemsPageLocators.SELECTED_SUPPLIER[1].replace("SUPPLIER_NAME", supplier_name))
        self.click(locator)

    def click_export_pos_button(self) -> None:
        """Click the 'Export POS' button."""
        self.click(ItemsPageLocators.EXPORT_POS_BUTTON)

    # =========================================================
    # GETTERS FOR ASSERTIONS IN TESTS
    # =========================================================

    def is_pos_file_downloaded(self, download_dir: str, timeout: int = 30) -> bool:
        """
        Wait for a POS file with the dynamic timestamp to appear in the download folder.

        Args:
            download_dir: The folder where POS files are downloaded.
            timeout: Maximum time (seconds) to wait for the download to complete.

        Returns:
            True if a completed POS file exists, False otherwise.
        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            # Find all files starting with 'pos_batch_'
            files = glob.glob(os.path.join(download_dir, "pos_batch_*"))
            if files:
                # Exclude any in-progress .tmp files
                completed_files = [f for f in files if not f.endswith(".tmp")]
                if completed_files:
                    # Latest fully downloaded file found
                    return True
            time.sleep(0.5)  # Wait briefly and retry

        return False  # Timeout reached without finding a complete file
