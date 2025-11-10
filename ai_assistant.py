import os
import re
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIAssistant:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI Assistant with OpenAI API."""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []
        
    def _should_use_web_search(self, query: str) -> bool:
        """Determine if the query requires web search."""
        # Keywords that suggest need for current information
        search_keywords = [
            "current", "latest", "recent", "today", "now", "what is", "who is",
            "where is", "when did", "how many", "news", "weather", "price",
            "stock", "score", "result", "happening", "update"
        ]
        
        query_lower = query.lower()
        # If it's asking for a story, creative content, or general knowledge, don't search
        if any(word in query_lower for word in ["tell me a story", "story", "joke", "poem", "creative"]):
            return False
        
        # Check if query contains search keywords
        return any(keyword in query_lower for keyword in search_keywords)
    
    def get_response(self, user_input: str, use_web_search: bool = False, web_context: Optional[str] = None) -> str:
        """Get AI response to user input."""
        # Build system message
        system_message = "You are a helpful AI assistant. You can answer questions, tell stories, have conversations, and provide information."
        
        if use_web_search and web_context:
            system_message += f"\n\nHere is some current information from the web:\n{web_context}\n\nUse this information to provide accurate and up-to-date answers."
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Prepare messages
        messages = [{"role": "system", "content": system_message}]
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages for context
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
