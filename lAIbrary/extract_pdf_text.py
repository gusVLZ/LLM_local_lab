import json
import fitz  # PyMuPDF
import re

from chroma_db import batch_insert

def split_text(text, delimiters):
    # Create a regular expression pattern with the given delimiters
    pattern = '|'.join(map(re.escape, delimiters))
    # Split the text using the pattern
    return re.split(pattern, text)

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    paragraphs = []
    meta = []
    ids = []
    
    # Iterate through each page
    for page_num in range(len(document)):
        localMeta = []
        localIds = []
        if(page_num<9 or page_num>262):
            continue
        page = document.load_page(page_num)
        text = page.get_text("text")
        
        # Split the text into paragraphs
        delimiters = ['\n\n', '.\n']
        page_paragraphs = split_text(text, delimiters)

        for i, p in enumerate(page_paragraphs):
            localMeta.append({
                "title": "História Medieval",
                "page": page_num,
                "paragraph": i,
                "subject": "history"
            })
            localIds.append(f"historiaMedieval:{page_num}:{i}")


        paragraphs.extend(page_paragraphs)
        meta.extend(localMeta)
        ids.extend(localIds)

    print("VERIFICANDO META X PARAGRAPH")
    print(len(paragraphs))
    print(len(meta))
    print("Exemplo meta ", meta[4])
    
    for i, p in enumerate(paragraphs):
        paragraphs[i] = paragraphs[i].replace("-\n", "")
        paragraphs[i] = paragraphs[i].replace("-\n ", "")
        paragraphs[i] = paragraphs[i].replace("\n", " ")
        paragraphs[i] = paragraphs[i].replace("  ", " ")
        paragraphs[i] = paragraphs[i].replace("___", "")
        paragraphs[i] = paragraphs[i].replace("___", "")
        paragraphs[i] = paragraphs[i].replace("___", "")
        paragraphs[i] = paragraphs[i].replace("__", "")

    return paragraphs, meta, ids

def insert_paragraphs_to_db():
    pdf_path = 'raw_data/medieval.pdf'
    print(pdf_path)
    paragraphs, meta, ids = extract_text_from_pdf(pdf_path)

    print("before insert")
    batch_insert(ids, paragraphs, meta)
    print("inserted, hopefully")
