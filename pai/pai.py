import sys
import subprocess
import os
import argparse
import uuid
from emitter import create_event, emit_event

def main():
    """
    Main orchestrator for the PAI CLI.
    Identifies the command and delegates to the appropriate skill script.
    """
    parser = argparse.ArgumentParser(description="PAI CLI")
    parser.add_argument("command", help="The command to execute.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for the command.")

    args = sys.argv[1:]

    if not args:
        parser.print_help()
        sys.exit(1)

    command = args[0]
    command_args = args[1:]

    # --- SECURITY: Command Allow-List ---
    allowed_commands = {"ask", "story"}
    if command not in allowed_commands:
        print(f"Error: Command '{command}' is not a valid command.")
        sys.exit(1)

    session_id = str(uuid.uuid4())
    event = create_event(
        source_app="pai-cli",
        hook_event_type=f"ExecuteSkill:{command}",
        payload={"command": command, "args": command_args},
        session_id=session_id
    )
    emit_event(event)

    skills_dir = os.path.join(os.path.dirname(__file__), 'skills')

    if command == "story":
        skill_path = os.path.join(skills_dir, "jules-the-storyteller.ts")
        interpreter = "bun"
        cwd = "blog"
        command_list = [interpreter, 'run', os.path.join('..', skill_path)] + command_args
    else:
        skill_path = os.path.join(skills_dir, f"{command}.py")
        interpreter = sys.executable
        cwd = None
        command_list = [interpreter, '-m', f'pai.skills.{command}'] + command_args

    if not os.path.exists(skill_path):
        print(f"Error: Command '{command}' not found.")
        sys.exit(1)

    try:
        env = os.environ.copy()
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            cwd=cwd
        )

        if process.stdout:
            for line in iter(process.stdout.readline, ''):
                print(line, end='', flush=True)

        stdout, stderr = process.communicate()

        if stderr:
            print(stderr, file=sys.stderr)

        if process.returncode != 0:
            print(f"Error executing command '{command}'.", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError:
        print(f"Error: '{interpreter}' interpreter not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
