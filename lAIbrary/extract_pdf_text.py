import fitz  # PyMuPDF
import re

def split_text(text, delimiters):
    # Create a regular expression pattern with the given delimiters
    pattern = '|'.join(map(re.escape, delimiters))
    # Split the text using the pattern
    return re.split(pattern, text)

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    paragraphs = []
    
    # Iterate through each page
    for page_num in range(len(document)):
        if(page_num<9 or page_num>262):
            continue
        page = document.load_page(page_num)
        text = page.get_text("text")
        
        # Split the text into paragraphs
        delimiters = ['\n\n', '.\n']
        page_paragraphs = split_text(text, delimiters)

        paragraphs.extend(page_paragraphs)
    
    return paragraphs

# Example usage
pdf_path = 'raw_data/medieval.pdf'
paragraphs = extract_text_from_pdf(pdf_path)

# Print the extracted paragraphs
for i, paragraph in enumerate(paragraphs):
    print(f"Paragraph {i+1}: {paragraph}\n")