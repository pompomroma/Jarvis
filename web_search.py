from duckduckgo_search import DDGS
from typing import Optional, List

class WebSearch:
    def __init__(self):
        """Initialize web search functionality."""
        self.ddgs = DDGS()
    
    def search(self, query: str, max_results: int = 5) -> Optional[str]:
        """
        Search the web for information.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted search results as string, or None if search fails
        """
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            
            if not results:
                return None
            
            # Format results
            formatted_results = []
            for i, result in enumerate(results[:max_results], 1):
                title = result.get('title', 'No title')
                snippet = result.get('body', 'No description')
                formatted_results.append(f"{i}. {title}\n   {snippet}")
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            print(f"Error during web search: {e}")
            return None
