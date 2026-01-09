"""
source_data.py
-----------------
Structured test data for the Sourcing page. Defines a small
Item dataclass and three item instances (`item1`, `item2`, `item3`) so
tests can reference them by name.

Usage:
  from data.source_data import SupplierData, item1, item2, item3

  supplier = SupplierData()
  items = [item1, item2, item3]
"""

from dataclasses import dataclass
from typing import Optional

# Brand
brand = [
    "Adidas",
    "Apple",
    "Generic",
    "Lee Plaza",
    "LG",
    "Nestle",
    "Nike",
    "Procter & Gamble",
    "Samsung",
    "Sony",
    "Unilever"
]

# Department
department = [
    "Beauty & Cosmetics",
    "Children's Fashion",
    "Electronics",
    "Food & Drinks",
    "Home Appliances",
    "Men's Fashion",
    "Office Supplies",
    "Outdoor Gear",
    "Sportswear",
    "Women's Fashion"
]

# Sub-Department
sub_department = [
    "Accessories",
    "Dresses",
    "Jackets",
    "Jeans",
    "Laptops",
    "Shoes",
    "Skirts",
    "Tablets",
    "T-shirts",
    "Watches"
]

# Category
category = [
    "Accessories",
    "Beauty & Cosmetics",
    "Children's Fashion",
    "Dresses",
    "Electronics",
    "Food & Drinks",
    "Home Appliances",
    "Jackets",
    "Jeans",
    "Laptops",
    "Men's Fashion",
    "Office Supplies",
    "Outdoor Gear",
    "Shoes",
    "Skirts",
    "Sportswear",
    "Tablets",
    "T-shirts",
    "Watches",
    "Women's Fashion"
]

# Item Group
item_group = [
    "Apparel & Fashion",
    "Automotive",
    "Electronics & Gadgets",
    "Food & Beverages",
    "Home & Living",
    "Jewelry & Watches",
    "Pet Supplies",
    "Sports & Outdoors",
    "Toys & Games"
]

# Sell Unit
sell_unit = [
    "BOX — Box",
    "CTN — Carton",
    "DOZ — Dozen",
    "G — Gram",
    "KG — Kilogram",
    "L — Liter",
    "M — Meter",
    "ML — Milliliter",
    "PKG — Package",
    "PAIR — Pair",
    "PC — Piece",
    "REAM — Ream",
    "ROLL — Roll",
    "SET — Set"
]

# Purchase Unit
purchase_unit = [
    "BOX — Box",
    "CTN — Carton",
    "DOZ — Dozen",
    "G — Gram",
    "KG — Kilogram",
    "L — Liter",
    "M — Meter",
    "ML — Milliliter",
    "PKG — Package",
    "PAIR — Pair",
    "PC — Piece",
    "REAM — Ream",
    "ROLL — Roll",
    "SET — Set"
]

# Size Category
size_category = [
    "American Size",
    "Bedding Size",
    "European Size",
    "Newborn",
    "One Size (Adjustable)",
    "One Size (Fixed)",
    "Plus Size",
    "Standard Sizing",
    "Teen Size"
]

# Color Category
color_category = [
    "Beige",
    "Black",
    "Blue",
    "Brown",
    "Clear",
    "Dark Blue",
    "Floral",
    "Gold",
    "Green",
    "Grey",
    "Light Wash",
    "Navy",
    "Pink",
    "Purple",
    "Red",
    "Rose Gold",
    "Silver",
    "White",
    "Yellow"
]

# Packaging
packaging = [
    "Blister Pack",
    "Box",
    "Individual Wrap",
    "Polybag with Hanger"
]

# Specification
specification = [
    "100% cotton material",
    "Cotton polyester blend",
    "Cotton elastane blend"
]

# Collection
collection = [
    "Fall 2025 Collection",
    "Spring 2025 Collection",
    "Winter 2025 Collection"
]

@dataclass(frozen=True)
class Item:
  name: str
  description: str
  brand: str
  department: str
  sub_department: str
  category: str
  item_group: str
  style: str
  selling_price: str
  sell_unit: str
  purchase_unit: str
  barcode_stock_no: str
  barcode: str
  size_category: Optional[str] = None
  color_category: Optional[str] = None
  packaging: Optional[str] = None
  specification: Optional[str] = None
  collection: Optional[str] = None
  remarks: Optional[str] = None


@dataclass(frozen=True)
class SupplierData:
  supplier_name: str
  supplier_address: str
  contact_person: str
  contact_address: str
  contact_number: str
  email: str
    

supplier1 = SupplierData(
  supplier_name="Automated Test Supplier #2 (Accept)",
  supplier_address="123 Test Street, Test City, TC 12345",
  contact_person="John Doe",
  contact_address="456 Contact Avenue, Contact City, CC 67890",
  contact_number="+1-555-0123",
  email="john1.doe@testsupplier.com"
)

supplier2 = SupplierData(
  supplier_name="Automated Test Supplier #2 (Reject)",
  supplier_address="123 Test Street, Test City, TC 12345",
  contact_person="Jane Smith",
  contact_address="789 Contact Road, Contact City, CC 67890",
  contact_number="+1-555-0456",
  email="jane1.smith@testsupplier.com"
)

# Define three distinct items for tests
item1 = Item(
  name="Performance Shoes",
  description="Lightweight running shoes for everyday training",
  brand=brand[0],
  department=department[3],
  sub_department=sub_department[5],
  category=category[13],
  item_group=item_group[7],
  style="Athletic Fit",
  selling_price="129.99",
  sell_unit=sell_unit[0],
  purchase_unit=purchase_unit[0],
  barcode_stock_no="20001",
  barcode="900000000001",
  size_category=size_category[2],
  color_category=color_category[17],
  packaging=packaging[1],
specification=specification[0],
  collection=collection[1],
  remarks="Auto-created test item 1",
)

item2 = Item(
  name="Item 2 - Casual Jacket",
  description="Comfortable denim jacket for casual wear",
  brand=brand[10],
  department=department[5],
  sub_department=sub_department[2],
  category=category[7],
  item_group=item_group[1],
  style="Slim Fit",
  selling_price="149.50",
  sell_unit=sell_unit[10],
  purchase_unit=purchase_unit[10],
  barcode_stock_no="20002",
  barcode="900000000002",
  size_category=size_category[0],
  color_category=color_category[2],
  packaging=packaging[3],
  specification=specification[1],
  collection=collection[0],
  remarks="Auto-created test item 2",
)

item3 = Item(
  name="Item 3 - Training Tee",
  description="Breathable tee for training and casual wear",
  brand=brand[6],
  department=department[5],
  sub_department=sub_department[8],
  category=category[17],
  item_group=item_group[1],
  style="Regular Fit",
  selling_price="39.99",
  sell_unit=sell_unit[10],
  purchase_unit=purchase_unit[10],
  barcode_stock_no="20003",
  barcode="900000000003",
  size_category=size_category[0],
  color_category=color_category[1],
  packaging=packaging[3],
  specification=specification[2],
  collection=collection[2],
  remarks="Auto-created test item 3",
)

edited_item2 = Item(
  name="Casual Jacket",
  description="Lightweight denim jacket suitable for everyday wear",
  brand=brand[8],
  department=department[4],
  sub_department=sub_department[1],
  category=category[6],
  item_group=item_group[0],
  style="Regular Fit",
  selling_price="129.00",
  sell_unit=sell_unit[8],
  purchase_unit=purchase_unit[8],
  barcode_stock_no="20002-EDIT",
  barcode="900000000102",
  size_category=size_category[1],
  color_category=color_category[1],
  packaging=packaging[2],
  specification=specification[0],
  collection=collection[1],
  remarks="Edited test item 2",
)


# Export a list for convenience
ALL_ITEMS = [item1, item2, item3]

# Default supplier instance
DEFAULT_SUPPLIER = supplier1
