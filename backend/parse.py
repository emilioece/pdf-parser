import PyPDF2
import json
import os
from pathlib import Path

def parse_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get the number of pages
            num_pages = len(pdf_reader.pages)
            print(f"Number of pages: {num_pages}")
            
            # Extract text from all pages
            all_text = ""
            for page_num in range(num_pages):
                # Get the page object
                page = pdf_reader.pages[page_num]
                # Extract text from the page
                all_text += page.extract_text()
                
            return all_text
    except FileNotFoundError:
        print(f"Error: The PDF file '{pdf_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_to_json(pdf_path, content):
    try:
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Get the PDF filename without extension and create json filename
        pdf_name = Path(pdf_path).stem
        json_path = output_dir / f"{pdf_name}.json"
        
        # Create a dictionary with the content
        data = {
            "filename": pdf_path,
            "content": content,
            "num_characters": len(content)
        }
        
        # Write to JSON file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
            
        print(f"JSON file created successfully: {json_path}")
        return True
        
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")
        return False

def main():
    # Parse the test PDF
    pdf_path = "test.pdf"
    print(f"Parsing PDF: {pdf_path}")
    text_content = parse_pdf(pdf_path)
    
    if text_content:
        print("\nExtracted text:")
        print(text_content)
        
        # Save the content to JSON
        save_to_json(pdf_path, text_content)

if __name__ == "__main__":
    main()