import os 
import fitz 
from docx import Document 
from langchain_community.document_loaders import pyPDFLoader
loader = PyPDFLoader("/home/teamsr/Desktop/agentic/autonomus_company_RA/knowledge/attn.pdf")
def read_documents(path):
    # how do we ensure that the [1] will get us extension ??
    extension = os.path.splitext(path)[1].lower()
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

