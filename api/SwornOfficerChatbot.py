from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API client with environment variable
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

if not PINECONE_API_KEY:
    raise ValueError("Missing required environment variable. Please ensure PINECONE_API_KEY is set in .env")

class ContentChatbot:
    def __init__(self):
        """Initialize the chatbot with Pinecone."""
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index("swornvideorecommendationsystem")
        self.conversation_history = []
        
    def chat(self, user_input):
        """
        Main chat function that processes user input and returns a response.
        
        Args:
            user_input (str): The user's input message
            
        Returns:
            str: The assistant's response
        """
        try:
            # Add message to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # For now, return a simple response
            response = f"I received your message: {user_input}"
            
            # Update conversation history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 6:
                self.conversation_history = self.conversation_history[-6:]
                
            return response
            
        except Exception as e:
            error_msg = f"Error processing chat: {str(e)}"
            print(error_msg)  # Log the error
            return f"I apologize, but I encountered an error. Please try again or rephrase your question."