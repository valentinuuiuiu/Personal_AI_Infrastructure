import os
import sys
from openai import OpenAI

def load_context() -> str:
    """
    Loads the personality context from the context directory.
    """
    try:
        # Construct the path to the context file relative to this script's location
        context_path = os.path.join(os.path.dirname(__file__), '..', 'context', 'personality.md')
        with open(context_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # If the context file is not found, return a default or empty string
        print("Warning: personality.md not found. Proceeding without system context.", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Error loading context: {e}", file=sys.stderr)
        return ""

# Get the API key from environment variables
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("Error: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1)

# Initialize the OpenAI client with the OpenRouter API base URL
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def ask_llm(prompt: str, context: str) -> str:
    """
    Sends a prompt to the specified LLM via OpenRouter and returns the response,
    including the system context.
    """
    messages = []
    if context:
        messages.append({"role": "system", "content": context})

    messages.append({"role": "user", "content": prompt})

    try:
        completion = client.chat.completions.create(
            model="minimax/minimax-m2:free",
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        system_context = load_context()
        user_prompt = " ".join(sys.argv[1:])
        response = ask_llm(user_prompt, system_context)
        print(response)
    else:
        print("Usage: python pai/skills/ask.py <your_prompt>")
