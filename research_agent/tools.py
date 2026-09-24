import requests 
from bs4 import BeautifulSoup
def get_definitions(query):
    print("searching for the ",query)
    results = {
        "transformers" : "Transformsers use self attention to process the relationship between words in a sentence. They are the backbone of many modern NLP models.",
        "rag": "RAG stands for Retrieval-Augmented Generation. It combines retrieval of relevant documents with generative models to produce more accurate and contextually relevant responses.",
        "agentic AI": "Agentic AI refers to artificial intelligence systems that can perform tasks autonomously, making decisions and taking actions without human intervention."
    }
    query_lower = query.lower()
    for key , value in results.items():
        if key in query_lower:
            return value

    return "No results found"


def calculator(expression):
   print("calculator called")
   print("expression: ", expression)
   try:
         result = str(eval(expression))
   except : 
       return "Error in calculation"

def search_web(query):
    print("searchig the web ")
    return f"Search results for :{query} \n"