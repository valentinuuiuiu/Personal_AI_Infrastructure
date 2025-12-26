import sys
import subprocess
import os

def main():
    """
    Main orchestrator for the PAI CLI.
    Identifies the command and delegates to the appropriate skill script.
    """
    if len(sys.argv) < 2:
        print("Usage: python pai/pai.py <command> [args...]")
        print("Available commands: ask, story")
        sys.exit(1)

    command = sys.argv[1]

    # --- SECURITY: Command Allow-List ---
    # Only allow known, safe commands to prevent path traversal.
    allowed_commands = {"ask", "story"}
    if command not in allowed_commands:
        print(f"Error: Command '{command}' is not a valid command.")
        sys.exit(1)

    args = sys.argv[2:]

    # Construct the path to the skills directory
    skills_dir = os.path.join(os.path.dirname(__file__), 'skills')

    if command == "story":
        skill_path = os.path.join(skills_dir, "jules-the-storyteller.ts")
        interpreter = "bun"
    else:
        skill_path = os.path.join(skills_dir, f"{command}.py")
        interpreter = "python3"

    if not os.path.exists(skill_path):
        print(f"Error: Command '{command}' not found.")
        sys.exit(1)

    # Execute the skill script as a subprocess, passing arguments
    try:
        # We need to pass the OPENROUTER_API_KEY to the subprocess environment
        env = os.environ.copy()

        # Ensure the correct interpreter is used for execution
        # For bun, we need to run it from the 'blog' directory to access node_modules
        cwd = 'blog' if interpreter == 'bun' else None
        command_list = [interpreter, 'run', os.path.join('..', skill_path)] + args if interpreter == "bun" else [interpreter, skill_path] + args

        process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            env=env,
            cwd=cwd
        )
        print(process.stdout, end='')
        if process.stderr:
            print(process.stderr, end='')

    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}':")
        print(e.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: 'python3' interpreter not found. Please make sure Python 3 is installed and in your PATH.")
        sys.exit(1)


if __name__ == "__main__":
    main()
