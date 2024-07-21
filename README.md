# Shopify Blog HTML Cleaner

Shopify Blog HTML Cleaner is a web application built with Flask that allows users to upload or paste HTML content, clean and modify it, and optionally save the modified HTML to a file. This tool is particularly useful for cleaning up HTML content for Shopify blogs.

## Features

- Upload HTML content via a TXT or CSV file
- Paste HTML content directly into the application
- Clean and modify HTML content using BeautifulSoup
- Save the modified HTML content to a file
- Copy the modified HTML content to the clipboard

## Requirements

- Python 3.x
- Flask
- BeautifulSoup4
- Werkzeug

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/shopify-blog-html-cleaner.git
    cd shopify-blog-html-cleaner
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:

    ```bash
    python app.py
    ```

5. **Open your web browser and navigate to** `http://127.0.0.1:5000`

## Usage

1. **Upload a file**: Click on the file input and select a TXT or CSV file containing HTML content.
2. **Paste HTML content**: Alternatively, you can paste HTML content directly into the provided textarea.
3. **Modify HTML**: The application will clean and modify the HTML content, which will be displayed in an editable textarea.
4. **Save to file**: Check the "Save to file" checkbox and click "Reprocess HTML" to save the modified HTML to a file.
5. **Copy to clipboard**: Click the "Copy to Clipboard" button to copy the modified HTM
