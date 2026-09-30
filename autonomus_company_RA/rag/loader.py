import os 
import fitz 
from docx import Document 

def read_documents(path):
    # how do we ensure that the [1] will get us extension ??
    extension = os.path.splittext(path)[1].lower()
    if extension == ".pdf":
        document = fitz.open(path)
        text = " "
        for page in document: 
            text+=page.get_text()
        document.close()
        return text 
    elif extension == ".docx":
        document = Document(path)
        return "\n".join(paragraph.text 
                         for paragraph in document.paragraphs)

    elif extension == ".txt":
        with open(path , "r",encoding = "utf-8") as file: 
            return file.read()
    else: 
        raise ValueError(f"file type not supported ")

