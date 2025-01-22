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
        """Initialize the chatbot with Pinecone assistant."""
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.assistant = self.pc.assistant.Assistant(
            assistant_name="sworn-content-assistant"
        )
        self.conversation_history = []
        
    def prepare_message(self, user_input):
        """Prepare the message for the assistant."""
        return Message(content=user_input)
        
    def chat(self, user_input, stream=False):
        """
        Main chat function that processes user input and returns a response.
        
        Args:
            user_input (str): The user's input message
            stream (bool): Whether to stream the response (default: False)
            
        Returns:
            str: The assistant's response
        """
        try:
            # Create message object
            message = self.prepare_message(user_input)
            
            # Add message to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Get response from assistant
            if stream:
                # Handle streaming response
                chunks = self.assistant.chat(messages=[message], stream=True)
                response_chunks = []
                for chunk in chunks:
                    if chunk:
                        response_chunks.append(chunk)
                response = "".join(response_chunks)
            else:
                # Handle regular response
                response_obj = self.assistant.chat(messages=[message])
                response = response_obj["message"]["content"]
            
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

def main():
    """Main function for testing the chatbot."""
    chatbot = ContentChatbot()
    
    print("Content Chatbot initialized. Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            break
            
        response = chatbot.chat(user_input)
        print("\nAssistant:", response)

if __name__ == "__main__":
    main()