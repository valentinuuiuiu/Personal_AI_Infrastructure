import os
import sys
import argparse
from ..llm_utils import call_llm

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

def run(args):
    """
    Main execution flow: get answer, optionally validate it, and yield the result.
    """
    user_prompt = " ".join(args.prompt)

    personality_context = load_context("personality")
    generation_messages = [
        {"role": "system", "content": personality_context},
        {"role": "user", "content": user_prompt}
    ]

    if args.stream:
        # Yield the response in chunks for streaming
        for chunk in call_llm(generation_messages, stream=True):
            yield chunk
    else:
        initial_answer = call_llm(generation_messages, stream=False)
        validator_context = load_context("validator")
        validation_prompt = f"Original Question: \"{user_prompt}\"\n\nResponse to Validate: \"{initial_answer}\""
        validation_messages = [
            {"role": "system", "content": validator_context},
            {"role": "user", "content": validation_prompt}
        ]
        validation_result = call_llm(validation_messages, stream=False).strip().upper()

        if "INVALID" in validation_result:
            validation_status = "INVALID"
        elif "VALID" in validation_result:
            validation_status = "VALID"
        else:
            validation_status = "UNKNOWN"

        yield f"[VALIDATION: {validation_status}] {initial_answer}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask the PAI a question.")
    parser.add_argument("--stream", action="store_true", help="Enable streaming response.")
    parser.add_argument("prompt", nargs='+', help="The prompt to send to the PAI.")
    args = parser.parse_args()

    for chunk in run(args):
        print(chunk, end='', flush=True)
    print()
