"""
OpenAI API Integration Module
Handles text generation and decision-making for the AI assistant
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIAssistant:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []
        
    def should_search_web(self, user_input):
        """
        Determines if web search is needed based on the user's query
        """
        # Keywords that suggest web search might be needed
        search_indicators = [
            'current', 'latest', 'news', 'today', 'weather', 
            'price', 'stock', 'who is', 'what is', 'when did',
            'search', 'look up', 'find information'
        ]
        
        user_input_lower = user_input.lower()
        
        # Check for explicit search requests
        for indicator in search_indicators:
            if indicator in user_input_lower:
                return True
        
        # Default to no search for creative tasks
        creative_indicators = ['tell me a story', 'write', 'create', 'imagine', 'describe']
        for indicator in creative_indicators:
            if indicator in user_input_lower:
                return False
                
        return False
    
    def generate_response(self, user_input, web_context=None):
        """
        Generate a response using OpenAI's API
        
        Args:
            user_input: The user's text input
            web_context: Optional context from web search
        
        Returns:
            AI-generated response text
        """
        # Build the message
        if web_context:
            system_message = f"""You are a helpful AI assistant with access to current information. 
Use the following web search results to help answer the user's question:

{web_context}

Provide a comprehensive and accurate answer based on this information."""
        else:
            system_message = """You are a helpful, creative, and intelligent AI assistant. 
You can engage in conversations, tell stories, answer questions based on your knowledge, 
and help with various tasks. Be friendly, informative, and engaging."""
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # Make API call
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_message},
                    *self.conversation_history[-10:]  # Keep last 10 messages for context
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
