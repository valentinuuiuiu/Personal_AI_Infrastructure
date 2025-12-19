import sys
import os
import argparse
import uuid
import importlib
import inspect
from emitter import create_event, emit_event

def execute_skill(skill_name, args):
    """
    Dynamically imports and executes a skill's run() function.
    Handles both regular and streaming (generator) functions.
    """
    try:
        module_name = f"pai.skills.{skill_name}"
        skill_module = importlib.import_module(module_name)

        result = skill_module.run(args)

        # Check if the result is a generator (for streaming)
        if inspect.isgenerator(result):
            yield from result
        else:
            yield result

    except ImportError:
        yield f"Error: Skill '{skill_name}' not found."
    except Exception as e:
        yield f"Error executing skill '{skill_name}': {e}"

def main():
    """
    Main orchestrator for the PAI CLI.
    """
    parser = argparse.ArgumentParser(description="PAI CLI")
    subparsers = parser.add_subparsers(dest='skill', required=True, help='The skill to execute.')

    parser_ask = subparsers.add_parser('ask', help='Ask the PAI a question.')
    parser_ask.add_argument("--stream", action="store_true", help="Enable streaming response.")
    parser_ask.add_argument("prompt", nargs='+', help="The prompt to send to the PAI.")

    parser_sharaba = subparsers.add_parser('sharaba', help='Analyze emotions from an image file.')
    parser_sharaba.add_argument("image_path", help="The full path to the image file to analyze.")

    args = parser.parse_args()

    session_id = str(uuid.uuid4())
    event = create_event(
        source_app="pai-cli",
        hook_event_type=f"ExecuteSkill:{args.skill}",
        payload={"skill": args.skill, "args": vars(args)},
        session_id=session_id
    )
    emit_event(event)

    # Execute the skill and handle streaming output
    is_first_chunk = True
    for chunk in execute_skill(args.skill, args):
        print(chunk, end='', flush=True)
        is_first_chunk = False

    # Print a final newline if there was any output
    if not is_first_chunk:
        print()

if __name__ == "__main__":
    main()
