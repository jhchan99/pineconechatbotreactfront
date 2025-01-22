import pinecone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone API client with environment variables
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')

if not PINECONE_API_KEY or not PINECONE_ENVIRONMENT:
    raise ValueError("Missing required environment variables. Ensure PINECONE_API_KEY and PINECONE_ENVIRONMENT are set in .env")

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

class ContentChatbot:
    def __init__(self):
        """Initialize the chatbot with Pinecone."""
        # Connect to or create a Pinecone index
        self.index_name = "sworn-content-assistant"
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name, dimension=512)  # Adjust dimensions based on embeddings
        self.index = pinecone.Index(self.index_name)
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
            # Add user input to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})

            # Mock logic for response generation
            # Replace this with actual logic using embeddings, GPT, or Pinecone queries
            assistant_reply = f"I received your message: {user_input}"
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_reply})

            # Keep conversation history manageable
            if len(self.conversation_history) > 6:
                self.conversation_history = self.conversation_history[-6:]

            return assistant_reply

        except Exception as e:
            error_msg = f"Error processing chat: {str(e)}"
            print(error_msg)  # Log the error
            return f"I apologize, but I encountered an error. Please try again or rephrase your question."

# Example usage
if __name__ == "__main__":
    chatbot = ContentChatbot()
    user_query = "How old is the earth?"
    
    # Non-streaming response
    response = chatbot.chat(user_query)
    print("Assistant response (non-streaming):", response)
