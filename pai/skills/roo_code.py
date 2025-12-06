import argparse
import sys
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'roo_code_config.json')

def load_config():
    """
    Loads the Roo Code configuration from the JSON file.
    """
    if not os.path.exists(CONFIG_FILE):
        return {"modes": [], "model_config": {}}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    """
    Saves the Roo Code configuration to the JSON file.
    """
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def main():
    """
    Main execution flow for the roo-code skill.
    """
    parser = argparse.ArgumentParser(description="A CLI for Roo Code, the AI-powered VS Code extension.")
    subparsers = parser.add_subparsers(dest="command", help="Available roo-code commands")

    # list-modes
    list_modes_parser = subparsers.add_parser("list-modes", help="List the available Roo Code modes.")

    # show-config
    show_config_parser = subparsers.add_parser("show-config", help="View the current model configuration.")

    # set-model
    set_model_parser = subparsers.add_parser("set-model", help="Set the model for a Roo Code mode.")
    set_model_parser.add_argument("--mode", required=True, help="The mode to configure.")
    set_model_parser.add_argument("--model", required=True, help="The model to use.")

    # create-mode
    create_mode_parser = subparsers.add_parser("create-mode", help="Create a new custom mode.")
    create_mode_parser.add_argument("name", help="The name of the new mode.")
    create_mode_parser.add_argument("--prompt", required=True, help="The system prompt for the new mode.")

    # mcp
    mcp_parser = subparsers.add_parser("mcp", help="Interact with an MCP server.")
    mcp_parser.add_argument("server", help="The name of the MCP server.")
    mcp_parser.add_argument("--prompt", required=True, help="The prompt to send to the MCP server.")

    # index
    index_parser = subparsers.add_parser("index", help="Index your codebase.")
    index_parser.add_argument("path", help="The path to the codebase to index.")

    # search
    search_parser = subparsers.add_parser("search", help="Perform a semantic search.")
    search_parser.add_argument("query", help="The semantic query to search for.")

    # browse
    browse_parser = subparsers.add_parser("browse", help="Automate browser interactions.")
    browse_parser.add_argument("url", help="The URL to navigate to.")
    browse_parser.add_argument("--prompt", required=True, help="The prompt for the browser automation.")

    if len(sys.argv) <= 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    config = load_config()

    if args.command == "list-modes":
        print("Available Roo Code modes:")
        for mode in config["modes"]:
            print(f"- {mode}")
    elif args.command == "show-config":
        print("Current model configuration:")
        for mode, model in config["model_config"].items():
            print(f"- {mode}: {model}")
    elif args.command == "set-model":
        if args.mode in config["model_config"]:
            config["model_config"][args.mode] = args.model
            save_config(config)
            print(f"Model for mode '{args.mode}' has been set to '{args.model}'.")
        else:
            print(f"Error: Mode '{args.mode}' not found.")
    elif args.command == "create-mode":
        if args.name in config["modes"]:
            print(f"Error: Mode '{args.name}' already exists.")
        else:
            config["modes"].append(args.name)
            config["model_config"][args.name] = "x-ai/grok-4-fast"  # Default model for new modes
            save_config(config)
            print(f"New mode '{args.name}' has been created.")
    elif args.command == "mcp":
        # In a real implementation, we would interact with the MCP server here.
        # For now, we will just print a message.
        print(f"Interacting with MCP server '{args.server}' with prompt: '{args.prompt}'...")
    elif args.command == "index":
        # In a real implementation, we would index the codebase here.
        # For now, we will just print a message.
        print(f"Indexing codebase at '{args.path}'...")
    elif args.command == "search":
        # In a real implementation, we would perform a semantic search here.
        # For now, we will just print a message.
        print(f"Searching for '{args.query}'...")
    elif args.command == "browse":
        # In a real implementation, we would automate browser interactions here.
        # For now, we will just print a message.
        print(f"Browsing to '{args.url}' with prompt: '{args.prompt}'...")
    else:
        parser.print_help(sys.stderr)

if __name__ == "__main__":
    main()
