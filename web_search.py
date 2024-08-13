import importlib.util
from typing import List, Dict, Optional
import openai
import os

class DuckDuckGoSearchToolSpec:
    spec_functions = ["duckduckgo_instant_search", "duckduckgo_full_search"]

    def __init__(self) -> None:
        if not importlib.util.find_spec("duckduckgo_search"):
            raise ImportError(
            )
        super().__init__()

    def duckduckgo_instant_search(self, query: str,  site: Optional[str] = None) -> List[Dict]:
        """
        Make a query to DuckDuckGo api to receive an instant answer.

        Args:
            query (str): The query to be passed to DuckDuckGo.
        """
        from duckduckgo_search import DDGS

        if site:
            query = f"site:{site} {query}"

        with DDGS() as ddg:
            return list(ddg.answers(query))

    def duckduckgo_full_search(
        self,
        query: str,
        site: Optional[str] = None,
        region: Optional[str] = "wt-wt",
        max_results: Optional[int] = 5,
    ) -> List[Dict]:
        """
        Make a query to DuckDuckGo search to receive a full search results.

        Args:
            query (str): The query to be passed to DuckDuckGo.
            region (Optional[str]): The region to be used for the search in [country-language] convention, ex us-en, uk-en, ru-ru, etc...
            max_results (Optional[int]): The maximum number of results to be returned.
        """
        from duckduckgo_search import DDGS

        if site:
            query = f"site:{site} {query}"

        params = {
            "keywords": query,
            "region": region,
            "max_results": max_results,
        }

        with DDGS() as ddg:
            return list(ddg.text(**params))

def search_with_openai_llm(api_key, query: str, search_type: str = "instant", site: Optional[str] = None) -> str:
    openai.api_key = api_key
    tool_spec = DuckDuckGoSearchToolSpec()
    
    if search_type == "instant":
        results = tool_spec.duckduckgo_instant_search(query, site=site)
    else:
        results = tool_spec.duckduckgo_full_search(query, site=site)

    # for i, result in enumerate(results):
    #     print(f"{i}: {result}")

    formatted_results = "\n".join([f"{i+1}. {result['title']}: {result.get('body', 'No body text')}" for i, result in enumerate(results)])

    response = openai.chat.completions.create(
        model='gpt-4o',
        messages=[
                {"role": "system", "content": 'You are an assistant skilled in giving the summary of news from multiple resources'},
                {"role": "user", "content": f"Provide a summary for the following search results:\n\n{formatted_results}\n\nSummary:"}
            ],
        temperature=0.3,
        max_tokens=2500
    )

    return  response.choices[0].message.content


def append_summary_to_files(api_key, directory: str, search_type: str = "instant", site: Optional[str] = None):
    """
    Iterate over all text files in the directory, extract the query from the file name,
    get the search results and summary, and append the summary to the corresponding text file.

    Args:
        directory (str): The directory containing the text files.
        search_type (str): The type of search to perform. Options are "instant" or "full".
        site (Optional[str]): The website to restrict the search to.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            query = filename.replace("_", " ").replace(".txt", "")
            summary = search_with_openai_llm(api_key, query, search_type, site)

            with open(os.path.join(directory, filename), "a", encoding = 'utf-8') as file:
                # file.write("\n")
                file.write(summary)

