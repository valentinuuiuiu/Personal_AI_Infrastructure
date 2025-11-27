import os
import sys
import subprocess
from openai import OpenAI

# Initialize the OpenAI client once
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Error: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def get_model_from_router(prompt: str) -> str:
    """
    Invokes the router skill to get the best model for the prompt.
    """
    try:
        router_path = os.path.join(os.path.dirname(__file__), 'router.py')
        # Use sys.executable to ensure the same interpreter is used
        process = subprocess.run(
            [sys.executable, router_path, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error calling router skill: {e.stderr}", file=sys.stderr)
        # Fallback to a default model in case the router fails
        return "mistralai/mistral-7b-instruct"
    except FileNotFoundError:
        print(f"Error: '{sys.executable}' not found.", file=sys.stderr)
        sys.exit(1)

def load_context(context_name: str) -> str:
    """
    Loads a specific context file from the context directory.
    """
    try:
        context_path = os.path.join(os.path.dirname(__file__), '..', 'context', f"{context_name}.md")
        with open(context_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {context_name}.md not found.", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Error loading context '{context_name}': {e}", file=sys.stderr)
        return ""

def call_llm(messages: list, model: str) -> str:
    """
    Sends a list of messages to the specified LLM and returns the content.
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    if len(sys.argv) <= 1:
        print("Usage: python pai/skills/ask.py <your_prompt>")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])

    # 1. Get the best model from the router
    model_to_use = get_model_from_router(user_prompt)
    print(f"--- Using model: {model_to_use} ---", file=sys.stderr)


    # 2. Generate the initial answer
    personality_context = load_context("personality")
    generation_messages = [
        {"role": "system", "content": personality_context},
        {"role": "user", "content": user_prompt}
    ]
    initial_answer = call_llm(generation_messages, model_to_use)

    # 3. Validate the answer
    validator_context = load_context("validator")
    validation_prompt = f"Original Question: \"{user_prompt}\"\n\nResponse to Validate: \"{initial_answer}\""
    validation_messages = [
        {"role": "system", "content": validator_context},
        {"role": "user", "content": validation_prompt}
    ]
    validation_result = call_llm(validation_messages, model_to_use).strip().upper()

    if "INVALID" in validation_result:
        validation_status = "INVALID"
    elif "VALID" in validation_result:
        validation_status = "VALID"
    else:
        validation_status = "UNKNOWN"

    # 4. Print the final, observable output
    print(f"[VALIDATION: {validation_status}] {initial_answer}")

if __name__ == "__main__":
    main()
