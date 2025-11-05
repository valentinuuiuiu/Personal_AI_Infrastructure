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
        print("Available commands: ask")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    # Construct the path to the skills directory
    skills_dir = os.path.join(os.path.dirname(__file__), 'skills')
    skill_path = os.path.join(skills_dir, f"{command}.py")

    if not os.path.exists(skill_path):
        print(f"Error: Command '{command}' not found.")
        sys.exit(1)

    # Execute the skill script as a subprocess, passing arguments
    try:
        # We need to pass the OPENROUTER_API_KEY to the subprocess environment
        env = os.environ.copy()

        # Ensure python3 is used for execution
        process = subprocess.run(
            ['python3', skill_path] + args,
            capture_output=True,
            text=True,
            check=True,
            env=env
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
