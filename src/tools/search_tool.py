import os
import json
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv
from serpapi import GoogleSearch
from agents import function_tool

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    raise RuntimeError("No SERPAPI_KEY provided")


@function_tool
def search_query(query: str) -> dict:
    """
    Executes a Google search and returns the results.

    Args:
        query (str): The text query to search on Google.

    Returns:
        dict: A dictionary containing the URLs of the search results.
    """

    params = {"q": query, "num": 50, "api_key": SERPAPI_KEY}

    search = GoogleSearch(params)
    results = search.get_dict()
    status = results.get("search_metadata", {}).get("status")
    links = results.get("organic_results", [])

    if status != "Success" or len(links) < 1:
        return {"msg": f"No results found for query {query}"}

    final_data = {
        "query": query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": [
            {
                "title": link["title"],
                "link": link["link"],
                "date": link.get("date", None),
                "position": link.get("position", 0),
            }
            for link in links
        ],
    }

    os.makedirs("./data", exist_ok=True)
    with open(
        f"./data/queries_{str(uuid4())}_{datetime.now().strftime('%y%m%d')}.json", "w+"
    ) as f:
        json.dump(final_data, f, indent=4, ensure_ascii=True)

    return final_data
