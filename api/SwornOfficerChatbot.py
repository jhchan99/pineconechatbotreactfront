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
        self.assistant = self.pc.assistant.Assistant(assistant_name="sworn-content-assistant")
        self.conversation_history = []

    def chat(self, user_input, stream=False):
        """
        Main chat function that processes user input and returns a response.
        
        Args:
            user_input (str): The user's input message
            stream (bool): Whether to use streaming for the response
            
        Returns:
            str or generator: The assistant's response or streaming chunks
        """
        try:
            # Create a message object for the user input
            user_message = Message(content=user_input)
            
            # Append message to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            if stream:
                # Stream response from assistant
                chunks = self.assistant.chat(messages=[user_message], stream=True)
                for chunk in chunks:
                    if chunk:
                        yield chunk
            else:
                # Get response from assistant
                response = self.assistant.chat(messages=[user_message])
                assistant_reply = response["message"]["content"]
                
                # Append assistant response to conversation history
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
    
    # Streaming response
    print("Assistant response (streaming):")
    for chunk in chatbot.chat(user_query, stream=True):
        print(chunk)
