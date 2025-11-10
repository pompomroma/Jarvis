"""
Web Search Module - Handles web searching functionality
"""
import requests
from bs4 import BeautifulSoup
import time

class WebSearch:
    def __init__(self):
        """Initialize web search"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query, num_results=5):
        """
        Search the web for information
        
        Args:
            query (str): Search query
            num_results (int): Number of results to return
            
        Returns:
            str: Formatted search results
        """
        try:
            print(f"🔍 Searching the web for: {query}")
            
            # Use DuckDuckGo HTML search (no API key needed)
            search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Find all result divs
                result_divs = soup.find_all('div', class_='result')
                
                for idx, result in enumerate(result_divs[:num_results]):
                    try:
                        # Extract title
                        title_elem = result.find('a', class_='result__a')
                        title = title_elem.get_text(strip=True) if title_elem else "No title"
                        
                        # Extract snippet
                        snippet_elem = result.find('a', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else "No description"
                        
                        # Extract URL
                        url = title_elem.get('href', '') if title_elem else ""
                        
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'url': url
                        })
                    except Exception as e:
                        continue
                
                # Format results
                if results:
                    formatted_results = self._format_results(results)
                    return formatted_results
                else:
                    return "No search results found."
            else:
                return f"Search failed with status code: {response.status_code}"
                
        except Exception as e:
            print(f"Error during web search: {e}")
            return f"Error performing web search: {str(e)}"
    
    def _format_results(self, results):
        """Format search results into a readable string"""
        formatted = "Web Search Results:\n\n"
        
        for idx, result in enumerate(results, 1):
            formatted += f"{idx}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n"
            if result['url']:
                formatted += f"   URL: {result['url']}\n"
            formatted += "\n"
        
        return formatted
    
    def quick_search(self, query):
        """
        Perform a quick search and return a summary
        
        Args:
            query (str): Search query
            
        Returns:
            str: Quick summary of search results
        """
        results = self.search(query, num_results=3)
        return results
    
    def fetch_page_content(self, url):
        """
        Fetch and extract text content from a webpage
        
        Args:
            url (str): URL to fetch
            
        Returns:
            str: Extracted text content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space
            lines = (line.strip() for line in text.splitlines())
            
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            
            # Drop blank lines
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Return first 2000 characters
            
        except Exception as e:
            return f"Error fetching page: {str(e)}"
