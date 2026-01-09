from ast import Tuple
from selenium.webdriver.common.by import By

# ============================================================
# UPDATE LOCATORS BELOW
# ============================================================


class SourcingPageLocators:
    """
    Locators for the Example Form page.

    - Replace these locators with real ones from your application.
    - This file is safe to copy and adapt for new pages.
    """

    # TODO: UPDATE THESE SELECTORS TO MATCH YOUR REAL APPLICATION
    NEW_SOURCE_BUTTON = (By.XPATH, "//button[contains(., 'New Source')]")

    # Add Source Form Locators
    SUPPLIER_NAME_INPUT = (By.ID, "supplierName")
    SUPPLIER_ADDRESS_INPUT = (By.ID, "supplierAddress")
    CONTACT_PERSON_INPUT = (By.ID, "contactPerson")
    CONTACT_ADDRESS_INPUT = (By.ID, "contactAddress")
    CONTACT_NUMBER_INPUT = (By.ID, "contactNumber")
    EMAIL_INPUT = (By.ID, "email")
    ADD_ATTACHMENT_BUTTON = (By.XPATH, "//input[@id='supplier-files']/preceding-sibling::button")
    ATTACHMENT_INPUT = (By.XPATH, "//input[@id='supplier-files']")
    ATTACHMENTS_CONTAINER = (By.XPATH, "//div[contains(@class, 'mt-3') and contains(@class, 'flex') and contains(@class, 'flex-wrap')]")
    
    ADD_ITEM_BUTTON = (By.XPATH, "//button[normalize-space()='+ Add Item']")
    
    ITEM_NAME_INPUT = (By.ID, "itemName")
    ITEM_DESCRIPTION_INPUT = (By.ID, "itemDescription")
    
    # Brand Dropdown
    BRAND_COMBO = (By.ID, "brand")
    BRAND_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    DEPARTMENT_COMBO = (By.ID, "department")
    DEPARTMENT_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    SUB_DEPARTMENT_COMBO = (By.ID, "subDepartment")
    SUB_DEPARTMENT_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    CATEGORY_COMBO = (By.ID, "category")
    CATEGORY_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    ITEM_GROUP_COMBO = (By.ID, "itemGroup")
    ITEM_GROUP_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    STYLE_COMBO = (By.ID, "style")
    STYLE_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')


    SELLING_PRICE = (By.ID, "sellingPrice")
    SELL_UNIT_COMBO = (By.ID, "sellUnit")
    SELL_UNIT_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')
    PURCHASE_UNIT_COMBO = (By.ID, "purchaseUnit")
    PURCHASE_UNIT_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')
    
    BARCODE_STOCK_NO_INPUT = (By.ID, "barcodeStockNo")
    BARCODE_INPUT = (By.ID, "barcode")

    SIZE_CATEGORY_COMBO = (By.ID, "sizeCategory")
    SIZE_CATEGORY_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    COLOR_CATEGORY_COMBO = (By.ID, "colorCategory")
    COLOR_CATEGORY_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    PACKAGING_COMBO = (By.ID, "packaging")
    PACKAGINGOPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    SPECIFICATION_COMBO = (By.ID, "specification")
    SPECIFICATION_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    COLLECTION_COMBO = (By.ID, "collection")
    COLLECTION_OPTION = (By.XPATH, '//div[@role="option" and contains(normalize-space(), "{option_name}")]')

    REMARKS_INPUT = (By.ID, "remarks")

    SAVE_ITEM_BUTTON = (By.XPATH, "//button[contains(normalize-space(), 'Save')]")
    UPDATE_ITEM_BUTTON = (By.XPATH, "//button[contains(normalize-space(), 'Update Item')]")
    CANCEL_ITEM_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    
    SELECTED_SUPPLIER = (By.XPATH, "//div[contains(@class,'overflow-y-auto')]//ul/li[.//span[text()='SUPPLIER_NAME']]")

    ITEM_CARD_BY_NAME = (By.XPATH, "//div[.//div[normalize-space()='{item_name}']]")
    EDIT_ITEM_BUTTON_BY_NAME = (By.XPATH, "//div[contains(@class,'flex lg:block gap-3')]/div[.//div[contains(normalize-space(.), '{item_name}')]]//div[contains(@class,'hidden lg:flex')]//button[1]")
    DELETE_ITEM_BUTTON_BY_NAME = (By.XPATH, "//div[.//div[normalize-space()='{item_name}']]//button[.//svg[contains(@class,'lucide-trash')]]")
    PUBLISH_BUTTON = (By.XPATH, "//button[contains(normalize-space(), 'Publish')]")

    MODAL_CANCEL_BUTTON = (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Cancel']")
    MODAL_CONFIRM_BUTTON = (By.XPATH, "//div[@role='dialog']//button[normalize-space()='Confirm']")

    #Notifications
    REJECTED_FILES = (By.XPATH, "//li[@data-sonner-toast and @data-type='error']//div[contains(text(),'Rejected files')]")
    SAVED_SUCCESSFULLY = (By.XPATH, "//li[@data-sonner-toast and @data-type='success']//div[contains(text(),'Supplier saved')]")
    INVALID_EMAIL = (By.XPATH, "//div[contains(@class,'border-red-200')]//p[normalize-space()='Please enter a valid email address.']")
    REQUIRED_CONTACT_EMAIL = (By.XPATH, "//div[contains(@class,'border-red-200')]//p[normalize-space()='Contact email is required.']")
    REQUIRED_SUPPLIER_NAME = (By.XPATH, "//div[contains(@class,'border-red-200')]//p[normalize-space()='Supplier name is required.']")
    NO_ITEM = (By.XPATH, "//div[contains(@class,'border-red-200')]//p[normalize-space()='Please add at least one item.']")
    ITEM_PRODUCT_NAME_REQUIRED = (By.XPATH, "//div[contains(@class,'border-red-200')]//p[normalize-space()='Item #{item_index}: product name is required.']")
    PUBLISHED_SUCCESSFULLY = (By.XPATH, "//li[@data-sonner-toast and @data-type='success']//div[contains(text(),'Published')]")

    #ADMIN CLERK ACCOUNT LOCATORS
    APPROVE_BUTTON = (By.XPATH, "//button[contains(@class,'bg-green-500') and normalize-space()='Approve']")
    REJECT_BUTTON = (By.XPATH, "//button[contains(@class,'bg-red-500') and normalize-space()='Reject']")

    REJECTION_REASON_INPUT = (By.XPATH, "//div[@role='dialog' and .//h2[normalize-space()='Reject Supplier']]//textarea")
    CONFIRM_REJECT_BUTTON = (By.XPATH, "//div[@role='dialog' and .//h2[normalize-space()='Reject Supplier']]//button[normalize-space()='Confirm Reject']")
    CANCEL_REJECT_BUTTON = (By.XPATH, "//div[@role='dialog' and .//h2[normalize-space()='Reject Supplier']]//button[normalize-space()='Cancel']")

    # Remove Item button for a specific item index. Use format(item_index=idx)
    REMOVE_ITEM_BUTTON = (By.XPATH, "(//div[contains(@class,'bg-gray-50') and contains(@class,'border-gray-200')]//button[normalize-space()='Remove Item'])[{item_index}]")
    # Container that holds item cards (use to count item blocks)
    ITEMS_CONTAINER = (By.XPATH, "//div[contains(@class,'bg-gray-50') and contains(@class,'border-gray-200')]")

    APPROVED_SUCCESSFULLY = (By.XPATH, "//li[@data-sonner-toast and @data-type='success']//div[contains(text(),'Approved')]")
    REJECTED_SUCCESSFULLY = (By.XPATH, "//li[@data-sonner-toast and @data-type='success']//div[contains(text(),'Rejected')]")

    SIGN_OUT_BUTTON = (By.XPATH, "//button[normalize-space()='Sign out']")