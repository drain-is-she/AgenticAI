from loader import read_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
text = read_documents(r"")
# without overlap just raw chunking 
# def chunk_text(text , chunk_size= 500 , overlap= 50 ):
#     words = text.split()
#     chunks = []
#     start = 0 
#     while(start<len(words)):
#         end = start+ chunk_size
#         chunk = " ".join(words[start:end])
#         chunks.append(chunk)
#         start+=chunk_size - overlap 
#     return chunks 


def chunk_text(text, chunk_size=100, overlap=20):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks

