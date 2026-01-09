"""
============================================================
 api_helper.py
============================================================

WHAT THIS FILE IS FOR
----------------------
- Provides utilities for making API requests and verification.
- Used to verify data saved via UI by querying API endpoints.

WHAT YOU SHOULD EDIT
--------------------
- Add new API helper methods as needed for your testing workflow.
"""

from __future__ import annotations

import requests
from typing import Any, Dict, Optional


class ItemSourcingAPI:
    """Helper class for Item Sourcing API calls."""

    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        """
        Initialize API helper.

        Args:
            base_url: Base URL of the API (e.g., "https://suppliersportal.macrosoft.services")
            auth_token: Authorization token for authenticated requests.
        """
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token
        self.headers = {
            "Content-Type": "application/json",
        }
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"

    def get_sourcing_requests(self, page_size: int = 200, page: int = 1) -> Dict[str, Any]:
        """
        Fetch list of sourcing requests from API.

        Args:
            page_size: Number of items per page.
            page: Page number (1-indexed).

        Returns:
            API response as dictionary.
        """
        url = f"{self.base_url}/api/ItemSourcing?pageSize={page_size}&page={page}"
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def find_sourcing_request_by_supplier_name(
        self, supplier_name: str, page_size: int = 200
    ) -> Optional[Dict[str, Any]]:
        """
        Find a sourcing request by supplier name.

        Args:
            supplier_name: Name of the supplier to search for.
            page_size: Number of items per page.

        Returns:
            The sourcing request dict if found, None otherwise.
        """
        response = self.get_sourcing_requests(page_size=page_size)
        data = response.get("data", [])

        for request in data:
            if request.get("supplierName") == supplier_name:
                return request

        return None

    def find_item_by_name_in_request(
        self, request: Dict[str, Any], item_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Find an item by name within a sourcing request.

        Args:
            request: Sourcing request dictionary.
            item_name: Name of the item to search for.

        Returns:
            The item dict if found, None otherwise.
        """
        items = request.get("items", [])
        for item in items:
            if item.get("itemName") == item_name:
                return item

        return None

    def verify_supplier_created(self, supplier_name: str) -> bool:
        """
        Verify that a supplier with the given name exists in the system.

        Args:
            supplier_name: Name of the supplier to verify.

        Returns:
            True if supplier found, False otherwise.
        """
        return self.find_sourcing_request_by_supplier_name(supplier_name) is not None

    def verify_item_in_supplier(self, supplier_name: str, item_name: str) -> bool:
        """
        Verify that an item exists under a specific supplier.

        Args:
            supplier_name: Name of the supplier.
            item_name: Name of the item.

        Returns:
            True if item found under supplier, False otherwise.
        """
        request = self.find_sourcing_request_by_supplier_name(supplier_name)
        if not request:
            return False

        return self.find_item_by_name_in_request(request, item_name) is not None
