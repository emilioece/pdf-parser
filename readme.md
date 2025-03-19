# PDF Page Number Extractor

A tool to extract and organize PDF pages based on their page numbers. This application can analyze your PDF documents, detect page numbers via OCR, and group pages with identical page numbers into separate PDF files.

## Features

- Extract page numbers from PDF documents using OCR
- Group pages with identical page numbers together
- Handle pages where page numbers can't be detected
- User-friendly graphical interface with drag-and-drop support
- Support for customizing output location

## Requirements

- Python 3.6 or higher
- Tesseract OCR

### Dependencies

- PyPDF2
- pytesseract
- pdf2image
- pillow
- tkinterdnd2 (for the GUI)
- packaging
- typing_extensions

## Installation

### Option 1: Using the Executable (Windows)

1. Download the latest release from the [releases page](link-to-releases)
2. Extract the ZIP file
3. Run the `PDF_Page_Extractor.exe` file

### Option 2: From Source

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pdf-page-extractor.git
   cd pdf-page-extractor
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   This will install all necessary Python packages with the correct versions.

4. Install Tesseract OCR:
   - **Windows**: Download and install from [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

## Usage

### GUI Application

1. Launch the application by running:
   ```
   python app.py
   ```

2. Either:
   - Click "Browse" to select your PDF file
   - Drag and drop your PDF onto the drop zone

3. Choose an output directory (optional)

4. Click "Parse PDF" to process the document

5. The application will create:
   - Separate PDFs for each detected page number in the output folder
   - An "unlabeled" folder for pages with no detectable page number

### Command Line

For batch processing or scripting:
