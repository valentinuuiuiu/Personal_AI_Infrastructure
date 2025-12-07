import os
import sys
from openai import OpenAI

_client = None

def get_client():
    """
    Initializes and returns the OpenAI client, creating it only once.
    """
    global _client
    if _client is None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            # We raise an exception here to be handled by the calling function
            raise ValueError("OPENROUTER_API_KEY environment variable not set.")

        _client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    return _client

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
        client = get_client()
        completion = client.chat.completions.create(
            model="x-ai/grok-4-fast",
            messages=messages,
            temperature=0.1, # Lower temperature for more predictable validation
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def call_llm_stream(messages: list):
    """
    Sends a list of messages to the LLM and yields the content chunks as they arrive.
    """
    try:
        client = get_client()
        stream = client.chat.completions.create(
            model="x-ai/grok-4-fast",
            messages=messages,
            stream=True,
            temperature=0.1,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        # Let the caller handle the exception to provide context
        raise e

def main():
    """
    Main execution flow: get answer, validate it, and print the result.
    Supports a --stream flag to bypass validation and stream the response.
    """
    try:
        stream_enabled = "--stream" in sys.argv
        if stream_enabled:
            sys.argv.remove("--stream")

        if len(sys.argv) <= 1:
            print("Usage: python pai/skills/ask.py [--stream] <your_prompt>")
            sys.exit(1)

        user_prompt = " ".join(sys.argv[1:])

        if stream_enabled:
            personality_context = load_context("personality")
            generation_messages = [
                {"role": "system", "content": personality_context},
                {"role": "user", "content": user_prompt}
            ]
            for chunk in call_llm_stream(generation_messages):
                print(chunk, end='', flush=True)
            print() # Ensure a final newline
        else:
            personality_context = load_context("personality")
            generation_messages = [
                {"role": "system", "content": personality_context},
                {"role": "user", "content": user_prompt}
            ]
            initial_answer = call_llm(generation_messages)

            validator_context = load_context("validator")
            validation_prompt = f"Original Question: \"{user_prompt}\"\n\nResponse to Validate: \"{initial_answer}\""
            validation_messages = [
                {"role": "system", "content": validator_context},
                {"role": "user", "content": validation_prompt}
            ]
            validation_result = call_llm(validation_messages).strip().upper()

            if "INVALID" in validation_result:
                validation_status = "INVALID"
            elif "VALID" in validation_result:
                validation_status = "VALID"
            else:
                validation_status = "UNKNOWN"

            print(f"[VALIDATION: {validation_status}] {initial_answer}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
