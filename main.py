import os
from together import Together
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

# Ensure API Key is set
if not API_KEY:
    raise ValueError("TOGETHER_API_KEY is missing. Set it in the .env file.")

# Initialize Together AI client
client = Together(api_key=API_KEY)

# Function to handle chatbot interaction
def chat_with_ai():
    print("💬 Welcome to the Together AI Chatbot! Type 'exit' to quit.\n")

    chat_history = []
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting... Have a great day!")
            break

        chat_history.append({"role": "user", "content": user_input})

        # Get AI response
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=chat_history,
            max_tokens=None,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>", "<|eom_id|>"],
            stream=True
        )

        print("AI: ", end="")
        ai_response = ""

        for token in response:
            if hasattr(token, "choices") and token.choices:
                text = token.choices[0].delta.content
                ai_response += text
                print(text, end="", flush=True)

        print("\n")
        chat_history.append({"role": "assistant", "content": ai_response})

# Run chatbot
if __name__ == "__main__":
    chat_with_ai()
