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

@dataclass
class ValidDocuments:
    # Valid files are in: D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS
    pdf_file: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS\TEST_PDF.pdf"
    doc_file: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS\TEST_DOC.doc"
    docx_file: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS\TEST_DOCX.docx"
    xls_file: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS\TEST_XLS.xls"
    xlsx_file: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS\TEST_XLSX.xlsx"
    ppt_file: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID DOCUMENTS\TEST_PPT.ppt"

@dataclass
class ValidImages:
    test_jpg: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID IMAGES\TEST_JPG.jpg"
    test_png: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID IMAGES\TEST_PNG.png"
    test_gif: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID IMAGES\TEST_GIF.gif"
    test_svg: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID IMAGES\TEST_SVG.svg"
    test_tiff: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID IMAGES\TEST_TIFF.tiff"
    test_webp: str = "D:\DIREC FILES\LEE PLAZA\TEST FILES\VALID IMAGES\TEST_WEBP.webp"


def get_valid_document_paths() -> str:
    """
    Retrieve all valid document file paths and join them with newlines.
    
    Returns a newline-separated string of all valid document paths from the ValidDocuments class.
    This is useful for bulk document attachment operations where multiple files need to be uploaded.
    
    Returns:
        str: Newline-separated string of all valid document file paths.
        
    Example:
        >>> paths = get_valid_document_paths()
        >>> paths
        'D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\VALID DOCUMENTS\\TEST_PDF.pdf\\nD:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\VALID DOCUMENTS\\TEST_DOC.doc\\n...'
    """
    documents = ValidDocuments()
    doc_paths = [
        documents.pdf_file,
        documents.doc_file,
        documents.docx_file,
        documents.xls_file,
        documents.xlsx_file,
        documents.ppt_file,
    ]
    return "\n".join(doc_paths)


def get_valid_image_paths() -> str:
    """
    Retrieve all valid image file paths and join them with newlines.
    
    Returns a newline-separated string of all valid image paths from the ValidImages class.
    This is useful for bulk image upload operations where multiple files need to be uploaded.
    
    Returns:
        str: Newline-separated string of all valid image file paths.
        
    Example:
        >>> paths = get_valid_image_paths()
        >>> paths
        'D:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\VALID IMAGES\\TEST_JPG.jpg\\nD:\\DIREC FILES\\LEE PLAZA\\TEST FILES\\VALID IMAGES\\TEST_PNG.png\\n...'
    """
    images = ValidImages()
    image_paths = [
        images.test_jpg,
        images.test_png,
        images.test_gif,
        images.test_svg,
        images.test_tiff,
        images.test_webp,
    ]
    return "\n".join(image_paths)