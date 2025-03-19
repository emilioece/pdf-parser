import re
import os
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
from pdf2image import convert_from_path

def extract_page_number(page_image):
    """
    Extract page number from a page image using OCR.
    Only looks at the bottom right corner of the page where page numbers are typically located.
    """
    # Get the dimensions of the page
    width, height = page_image.size
    
    # Define the region of interest (bottom right corner)
    # Adjusted for better capture of small, standalone page numbers
    right_margin = int(width * 0.3)  # Right 30% of the page (increased)
    bottom_margin = int(height * 0.15)  # Bottom 15% of the page (increased)
    
    # Crop the image to the region of interest
    crop_box = (width - right_margin, height - bottom_margin, width, height)
    corner_image = page_image.crop(crop_box)
    
    # Save the cropped image for debugging (optional)
    # corner_image.save(f"debug_corner_{os.getpid()}.png")
    
    # Convert to text using OCR with specific configuration for numbers
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(corner_image, config=custom_config)
    
    # Print raw OCR result for debugging
    print(f"Raw OCR text: '{text.strip()}'")
    
    # Look for patterns that might represent page numbers
    # This regex looks for standalone numbers, which are likely page numbers
    matches = re.findall(r'(\d+)', text)
    
    # Return the first match if found, otherwise None
    if matches:
        return matches[0]
    
    # Additional check for single digit that might be missed
    if re.search(r'[0-9]', text):
        return re.search(r'[0-9]', text).group(0)
    
    return None

def process_pdf(input_pdf_path, output_dir="output"):
    """Process the PDF and split it based on page numbers."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create unlabeled subfolder if it doesn't exist
    unlabeled_dir = os.path.join(output_dir, "unlabeled")
    os.makedirs(unlabeled_dir, exist_ok=True)
    
    # Convert PDF pages to images for OCR
    images = convert_from_path(input_pdf_path)
    
    # Open the original PDF
    reader = PdfReader(input_pdf_path)
    
    # Dictionary to store pages grouped by page number
    page_groups = {}
    
    # Process each page
    for i, (page, image) in enumerate(zip(reader.pages, images)):
        print(f"Processing page {i+1} of {len(reader.pages)}...")
        
        # Extract page number using OCR
        page_number = extract_page_number(image)
        
        print(f"  → Detected page number: {page_number}")
        
        if page_number is None:
            print(f"Could not extract page number from page {i+1}")
            # Add to special "unlabeled" group instead of skipping
            if "unlabeled" not in page_groups:
                page_groups["unlabeled"] = []
            page_groups["unlabeled"].append((i, page))
            continue
        
        # Add page to its group
        if page_number not in page_groups:
            page_groups[page_number] = []
        
        page_groups[page_number].append((i, page))
    
    # Create separate PDFs for each page number
    for page_number, pages in page_groups.items():
        writer = PdfWriter()
        
        for i, page in pages:
            writer.add_page(page)
        
        # Handle unlabeled pages differently - save in unlabeled subfolder
        if page_number == "unlabeled":
            output_path = os.path.join(unlabeled_dir, "unlabeled.pdf")
        else:
            output_path = os.path.join(output_dir, f"page_{page_number}.pdf")
            
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        print(f"Created {output_path} with {len(pages)} pages")

if __name__ == "__main__":
    process_pdf("test.pdf")
