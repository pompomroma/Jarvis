"""
Web Search Module
Handles web searching using DuckDuckGo
"""

from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

class WebSearch:
    def __init__(self):
        self.ddg = DDGS()
    
    def search(self, query, max_results=3):
        """
        Search the web using DuckDuckGo
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
        
        Returns:
            String containing formatted search results
        """
        try:
            print(f"🔍 Searching the web for: {query}")
            
            # Perform search
            results = list(self.ddg.text(query, max_results=max_results))
            
            if not results:
                return "No search results found."
            
            # Format results
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                url = result.get('href', '')
                
                formatted_results.append(
                    f"Result {i}:\n"
                    f"Title: {title}\n"
                    f"Description: {body}\n"
                    f"URL: {url}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            print(f"❌ Error during web search: {e}")
            return f"Search error: {str(e)}"
    
    def quick_search(self, query):
        """
        Perform a quick search and return a concise summary
        
        Args:
            query: Search query string
        
        Returns:
            Concise string with top results
        """
        try:
            results = list(self.ddg.text(query, max_results=5))
            
            if not results:
                return None
            
            # Get the most relevant information
            summaries = []
            for result in results[:3]:
                body = result.get('body', '')
                if body:
                    summaries.append(body)
            
            return " ".join(summaries)
            
        except Exception as e:
            return None
    
    def search_news(self, query, max_results=3):
        """
        Search for news articles
        
        Args:
            query: Search query string
            max_results: Maximum number of results
        
        Returns:
            Formatted news results
        """
        try:
            print(f"📰 Searching news for: {query}")
            
            results = list(self.ddg.news(query, max_results=max_results))
            
            if not results:
                return "No news results found."
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                body = result.get('body', 'No description')
                date = result.get('date', 'Unknown date')
                source = result.get('source', 'Unknown source')
                
                formatted_results.append(
                    f"News {i}:\n"
                    f"Title: {title}\n"
                    f"Source: {source}\n"
                    f"Date: {date}\n"
                    f"Description: {body}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            print(f"❌ Error during news search: {e}")
            return f"News search error: {str(e)}"
