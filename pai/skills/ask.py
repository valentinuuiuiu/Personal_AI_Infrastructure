import os
import sys
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

def load_context(context_name: str) -> str:
    """
    Loads a specific context file from the context directory.
    """
    try:
        context_path = os.path.join(os.path.dirname(__file__), '..', 'context', f"{context_name}.md")
        with open(context_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {context_name}.md not found. Proceeding without this context.", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Error loading context '{context_name}': {e}", file=sys.stderr)
        return ""

def call_llm(messages: list) -> str:
    """
    Sends a list of messages to the LLM and returns the content of the response.
    """
    try:
        completion = client.chat.completions.create(
            model="minimax/minimax-m2:free",
            messages=messages,
            temperature=0.1, # Lower temperature for more predictable validation
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    """
    Main execution flow: get answer, validate it, and print the result.
    """
    if len(sys.argv) <= 1:
        print("Usage: python pai/skills/ask.py <your_prompt>")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])

    # 1. Generate the initial answer
    personality_context = load_context("personality")
    generation_messages = [
        {"role": "system", "content": personality_context},
        {"role": "user", "content": user_prompt}
    ]
    initial_answer = call_llm(generation_messages)

    # 2. Validate the answer
    validator_context = load_context("validator")
    validation_prompt = f"Original Question: \"{user_prompt}\"\n\nResponse to Validate: \"{initial_answer}\""
    validation_messages = [
        {"role": "system", "content": validator_context},
        {"role": "user", "content": validation_prompt}
    ]
    validation_result = call_llm(validation_messages).strip().upper()

    # Clean up validation result to be robust
    if "INVALID" in validation_result:
        validation_status = "INVALID"
    elif "VALID" in validation_result:
        validation_status = "VALID"
    else:
        validation_status = "UNKNOWN" # Fallback if the validator doesn't behave

    # 3. Print the final, observable output
    print(f"[VALIDATION: {validation_status}] {initial_answer}")

if __name__ == "__main__":
    main()
