import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file (force reload)
load_dotenv(override=True)

# Get API key and model name from environment variables
api_key = os.getenv("OPENROUTER_API_KEY")
model_name = os.getenv("MODEL_NAME")

# Display debug information
print(f"Loaded environment variables:")
print(f"MODEL_NAME: {model_name}")

# Check if API key and model name are set
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the .env file")
if not model_name:
    raise ValueError("MODEL_NAME is not set in the .env file")

# OpenRouter API endpoint
api_url = "https://openrouter.ai/api/v1/chat/completions"

# Set headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost",  # OpenRouter requires this
    "X-Title": f"OpenRouter Chat with {model_name}"    # Optional: your app name
}

def chat_with_model(messages):
    """
    Function to chat with a model using the OpenRouter API
    
    Args:
        messages: Conversation history
        
    Returns:
        Response text from the model
    """
    payload = {
        "model": model_name,
        "messages": messages
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception if there is an error
        
        response_data = response.json()
        assistant_message = response_data["choices"][0]["message"]["content"]
        return assistant_message
    
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return "An error occurred. Please try again."

def main():
    """
    Main conversation loop
    """
    print(f"Starting conversation with {model_name}. Type 'exit' to end.")
    print(f"Using model: {model_name}")
    
    # Conversation history
    messages = []
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check exit command
        if user_input.lower() in ["exit", "quit", "end"]:
            print("Ending conversation.")
            break
        
        # Add user message to conversation history
        messages.append({"role": "user", "content": user_input})
        
        # Call API to get model response
        assistant_response = chat_with_model(messages)
        
        # Display assistant response
        print(f"\nAssistant: {assistant_response}")
        
        # Add assistant message to conversation history
        messages.append({"role": "assistant", "content": assistant_response})

if __name__ == "__main__":
    main()