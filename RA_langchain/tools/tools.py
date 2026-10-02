def search_web(query):
    print("searching for the query") 
    return f"Dummy search result for :{query}"
def calculator(expression):
    return f"{expression}"
def get_stock_price(company):
    return f"{company}"
def get_company_info(company):
    return f"The report of the {company}"
def fetch_webpage(url):
    return f"{url} results"
def save_report(info):
    return f" saved report "
def search_knowledge_base(pdf) : 
    return f"{pdf}"
TOOLS = {
    "search_web": search_web , 
    "calculator " : calculator , 
    "get_stock_price": get_stock_price , 
    "get_company_info": get_company_info ,
    "fetch_webpage" : fetch_webpage ,
    "save_report" :save_report  , 
    "search_knowledge_base" : search_knowledge_base , 

}

