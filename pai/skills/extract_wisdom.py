import argparse
import sys
import os
import requests
from ..llm_utils import call_llm

def load_pattern(pattern_name: str) -> str:
    """
    Loads the system prompt from a pattern's markdown file.
    """
    pai_dir = os.environ.get('PAI_DIR', os.path.join(os.path.expanduser('~'), '.claude'))
    try:
        pattern_path = os.path.join(pai_dir, 'skills', 'fabric', 'fabric-repo', 'data', 'patterns', pattern_name, 'system.md')
        with open(pattern_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Pattern '{pattern_name}' not found.", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Error loading pattern '{pattern_name}': {e}", file=sys.stderr)
        return ""

def main():
    """
    Main execution flow for the extract_wisdom skill.
    """
    parser = argparse.ArgumentParser(description="Extract wisdom from a piece of content.")
    parser.add_argument("--text", help="The text content to process.")
    parser.add_argument("--url", help="The URL of the content to process.")
    parser.add_argument("--stream", action="store_true", help="Enable streaming response.")

    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if not args.text and not args.url:
        print("Error: Either --text or --url must be provided.", file=sys.stderr)
        sys.exit(1)

    if args.url:
        try:
            response = requests.get(args.url)
            response.raise_for_status()
            input_content = response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        input_content = args.text

    system_prompt = load_pattern("extract_wisdom")
    if not system_prompt:
        sys.exit(1)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_content}
    ]

    if args.stream:
        for chunk in call_llm(messages, stream=True):
            print(chunk, end='', flush=True)
        print()
    else:
        print(call_llm(messages, stream=False))

if __name__ == "__main__":
    main()
