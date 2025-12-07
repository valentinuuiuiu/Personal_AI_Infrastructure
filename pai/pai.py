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

    # Determine if streaming is requested
    stream_enabled = "--stream" in args

    try:
        env = os.environ.copy()
        cmd = ['python3', skill_path] + args

        if stream_enabled:
            # For streaming, we need to handle stdout line by line
            with subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                bufsize=1,
                universal_newlines=True
            ) as process:
                # Stream stdout
                for line in process.stdout:
                    print(line, end='', flush=True)

                # Wait for the process to finish and capture stderr
                stderr_output = process.communicate()[1]
                if process.returncode != 0:
                    print(f"\nError executing command '{command}':", file=sys.stderr)
                    if stderr_output:
                        print(stderr_output, file=sys.stderr)
                    sys.exit(process.returncode)
        else:
            # For non-streaming, we can use the simpler subprocess.run
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            print(result.stdout, end='')
            if result.stderr:
                print(result.stderr, file=sys.stderr, end='')

    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}':", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'python3' interpreter not found. Please make sure Python 3 is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
