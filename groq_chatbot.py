import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

headers = lambda: {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '')}",
    "Content-Type": "application/json"
}

def chat_with_groq(messages):
    if not os.getenv("GROQ_API_KEY"):
        raise Exception("GROQ_API_KEY not set in environment.")
    payload = {
        "model": MODEL,
        "messages": messages
    }
    response = requests.post(GROQ_API_URL, headers=headers(), json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    print("Welcome to the Groq AI Chatbot (Llama-3-8b)")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        try:
            reply = chat_with_groq(messages)
            print(f"Groq: {reply}")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
