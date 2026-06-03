import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def extract_text(results):
    """
    Pulls out just the text content from tavily search results
    """
    return "\n\n".join(
            r["content"] for r in results.get("results", []))

def gather_data(data):
    """
    Agent1: Searches the live web for financial, news, and leadership information about the target company
    """

    company_name = data["company_name"]
    print(f"Gathering live data about {company_name}...")

    financial_results = tavily.search(query=f"{company_name} financial health revenue profit 2024 2025", max_results=4)
    news_results = tavily.search(query=f"{company_name} latest news risk controversy lawsuit 2025", max_results=4)
    leadership_results = tavily.search(query=f"{company_name} CEO founder ownership structure board", max_results=3)
    data["financial_info"] = extract_text(financial_results)
    data["news_info"] = extract_text(news_results)
    data["leadership_info"] = extract_text(leadership_results)
    print("Live data collected ...")
    return data

