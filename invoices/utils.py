import pytesseract
from PIL import Image
import re

def extract_invoice_data(image_path):
    """
    Enhanced AI Brain: Uses multi-pattern matching to find 
    Vendors, Totals, and Dates with high accuracy.
    """
    # Open the image
    img = Image.open(image_path)
    
    # Use 'Sparse Text' config for better performance on structured documents like invoices
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, config=custom_config)
    
    # --- 1. THE TOTAL AMOUNT FINDER ---
    # We use a list of common 'Total' keywords found in accounting
    total_patterns = [
        r"(?:Total|TOTAL|Amount Due|Balance Due|Grand Total|Net Payable)[:\s]*\$?\s*([\d,]+\.\d{2})",
        r"\$\s*([\d,]+\.\d{2})" # Fallback: any dollar amount with decimals
    ]
    
    total_amount = "0.00"
    for pattern in total_patterns:
        match = re.search(pattern, text)
        if match:
            # Take the first group, remove commas for DecimalField compatibility
            total_amount = match.group(1).replace(',', '')
            break

    # --- 2. THE VENDOR FINDER ---
    # Usually, the vendor is at the very top. We look for the first line that isn't just numbers.
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 2]
    vendor_name = "Unknown Vendor"
    
    # Check top 5 lines for something that looks like a Company Name
    for line in lines[:5]:
        # If the line doesn't start with a number (like an address or date) it's likely the Vendor
        if not re.match(r'^\d', line):
            vendor_name = line
            break

    # --- 3. THE DATE FINDER ---
    # Matches 01/01/2026, 2026-01-01, or Jan 01, 2026
    date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|([A-Z][a-z]{2,8}\s\d{1,2},?\s\d{4})"
    date_match = re.search(date_pattern, text)
    extracted_date = date_match.group(0) if date_match else None

    return {
        "vendor_name": vendor_name,
        "total_amount": total_amount,
        "date": extracted_date,
        "raw_text": text
    }
    
    # invoices/utils.py

def perform_ai_extraction(file):
    """
    Temporary placeholder for AI extraction logic.
    In the next step, we will connect this to Gemini or Tesseract.
    """
    return {
        'vendor_name': 'Demo Vendor Inc',
        'invoice_date': '2026-01-13',
        'invoice_number': 'INV-12345',
        'total_amount': '150.00',
        'currency': 'USD',
    }