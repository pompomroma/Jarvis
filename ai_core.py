"""
AI Core Module - Handles OpenAI API interactions
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AICore:
    def __init__(self):
        """Initialize OpenAI client with API key"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []
        
    def chat(self, user_message, use_web_search=False, search_results=None):
        """
        Send a message to the AI and get a response
        
        Args:
            user_message (str): The user's message
            use_web_search (bool): Whether web search results should be included
            search_results (str): Web search results to include in context
            
        Returns:
            str: AI's response
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # If web search is enabled and we have results, prepend them to the message
            if use_web_search and search_results:
                enhanced_message = f"""Based on the following web search results, please answer the user's question.

Web Search Results:
{search_results}

User Question: {user_message}

Please provide a comprehensive answer based on the search results above."""
                
                # Replace the last message with the enhanced version
                self.conversation_history[-1]["content"] = enhanced_message
            
            # Create chat completion
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a helpful, intelligent, and versatile AI assistant. 
You can engage in conversations, answer questions, tell stories, provide information, and assist with various tasks.
When you receive information from web searches, use it to provide accurate and up-to-date answers.
When no web search is needed (like telling stories, having conversations, or answering general knowledge questions), 
rely on your training data. Be friendly, informative, and engaging."""}
                ] + self.conversation_history,
                temperature=0.7,
            )
            
            # Get the assistant's response
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."
    
    def get_history_length(self):
        """Get the number of messages in history"""
        return len(self.conversation_history)
