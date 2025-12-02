# Roo Code Training Program: A Guide to AI-Assisted Development

This training program will guide you through the process of mastering Roo Code, the AI-powered VS Code extension. You will learn how to use Roo Code to write, debug, and deploy software more effectively. This guide incorporates "triggers" for reinforced learning, using the `jules-cli` to provide a hands-on experience.

## Module 1: Foundation

This module covers the basics of Roo Code, including installation, setup, and understanding the core architecture.

### 1.1 Installation and Setup

**Objective:** Install Roo Code and the `jules-cli` and connect your accounts.

**Instructions:**

1.  **Install Roo Code:** Install the Roo Code extension from the VS Code Marketplace.
2.  **Install `jules-cli`:** Follow the instructions in the `jules-cli` documentation to install the CLI.
3.  **Connect Accounts:** Connect your Roo Code and `jules-cli` to your GitHub account.

**Trigger:**

*   **Task:** Verify your installation.
*   **Command:**
    ```bash
    jules-cli --version
    ```
*   **Expected Outcome:** The `jules-cli` version number is printed to the console.

### 1.2 Understanding the Five-Mode Architecture

**Objective:** Understand the purpose of each of Roo Code's five modes.

**Instructions:** Read the "Five Modes Deep Dive" section of the Roo Code documentation.

**Trigger:**

*   **Task:** Use the `jules-cli` to list the available Roo Code modes.
*   **Command:**
    ```bash
    jules-cli roo-code --list-modes
    ```
*   **Expected Outcome:** A list of the five Roo Code modes is printed to the console.

### 1.3 Model Selection Strategies

**Objective:** Understand how to select the right AI model for each task.

**Instructions:** Read the "Model Selection" section of the Roo Code documentation.

**Trigger:**

*   **Task:** Use the `jules-cli` to view the current model configuration.
*   **Command:**
    ```bash
    jules-cli roo-code --show-config
    ```
*   **Expected Outcome:** The current model configuration is printed to the console.

### 1.4 Optimal Configuration

**Objective:** Learn how to configure Roo Code for optimal performance.

**Instructions:** Read the "Optimal Configuration" section of the Roo Code documentation.

**Trigger:**

*   **Task:** Use the `jules-cli` to set the model for the "Code Mode" to "Claude Sonnet 4".
*   **Command:**
    ```bash
    jules-cli roo-code --set-model --mode "Code Mode" --model "Claude Sonnet 4"
    ```
*   **Expected Outcome:** The model for the "Code Mode" is updated. You can verify this by running `jules-cli roo-code --show-config` again.

## Module 2: The Five Modes Deep Dive

This module provides a deep dive into each of Roo Code's five modes.

### 2.1 Code Mode

**Objective:** Learn how to use the "Code Mode" to write and refactor code.

**Trigger:**

*   **Task:** Create a new file called `example.py` and add a simple "hello world" function. Then, use the `jules-cli` to refactor the function to take a name as an argument and print "Hello, [name]".
*   **Command:**
    1.  Create `example.py` with the following content:
        ```python
        def hello():
            print("Hello, world!")
        ```
    2.  Run the following command:
        ```bash
        jules-cli roo-code --mode "Code Mode" --prompt "Refactor the hello function in example.py to take a name as an argument and print 'Hello, [name]'."
        ```
*   **Expected Outcome:** The `example.py` file is updated with the refactored function.

### 2.2 Architect Mode

**Objective:** Learn how to use the "Architect Mode" to plan complex features.

**Trigger:**

*   **Task:** Use the `jules-cli` to create a plan for a new feature that adds a new endpoint to a web application.
*   **Command:**
    ```bash
    jules-cli roo-code --mode "Architect Mode" --prompt "Create a plan to add a new endpoint called '/hello' to a Flask application. The endpoint should return a JSON object with the message 'Hello, world!'."
    ```
*   **Expected Outcome:** A plan for the new feature is printed to the console.

### 2.3 Ask Mode

**Objective:** Learn how to use the "Ask Mode" to get answers to your coding questions.

**Trigger:**

*   **Task:** Use the `jules-cli` to ask a question about the Flask web framework.
*   **Command:**
    ```bash
    jules-cli roo-code --mode "Ask Mode" --prompt "How do I get the value of a query parameter in a Flask application?"
    ```
*   **Expected Outcome:** An answer to your question is printed to the console.

### 2.4 Debug Mode

**Objective:** Learn how to use the "Debug Mode" to find and fix bugs in your code.

**Trigger:**

*   **Task:** Create a new file called `buggy.py` with a bug in it. Then, use the `jules-cli` to find and fix the bug.
*   **Command:**
    1.  Create `buggy.py` with the following content:
        ```python
        def add(a, b):
            return a - b
        ```
    2.  Run the following command:
        ```bash
        jules-cli roo-code --mode "Debug Mode" --prompt "The add function in buggy.py is not working correctly. It should add two numbers, but it is subtracting them instead. Please fix the bug."
        ```
*   **Expected Outcome:** The `buggy.py` file is updated with the corrected function.

### 2.5 Orchestrator Mode

**Objective:** Learn how to use the "Orchestrator Mode" to manage complex workflows.

**Trigger:**

*   **Task:** Use the `jules-cli` to create a workflow that first plans a new feature and then implements it.
*   **Command:**
    ```bash
    jules-cli roo-code --mode "Orchestrator Mode" --prompt "First, create a plan to add a new endpoint called '/greet' to a Flask application. The endpoint should return a JSON object with the message 'Greetings!'. Then, implement the new endpoint."
    ```
*   **Expected Outcome:** A plan for the new feature is created, and then the new endpoint is implemented.

## Module 3: Advanced Features

This module covers the advanced features of Roo Code, including custom modes and MCP server integration.

### 3.1 Custom Mode Creation and Configuration

**Objective:** Learn how to create and configure custom modes in Roo Code.

**Trigger:**

*   **Task:** Create a new custom mode called "Docstring Generator" that automatically generates docstrings for Python functions.
*   **Command:**
    ```bash
    jules-cli roo-code --create-mode "Docstring Generator" --prompt "You are a helpful AI assistant that generates docstrings for Python functions. You should follow the Google Python Style Guide for docstrings."
    ```
*   **Expected Outcome:** A new custom mode is created. You can verify this by running `jules-cli roo-code --list-modes`.

### 3.2 MCP (Model Context Protocol) Server Integration

**Objective:** Learn how to integrate Roo Code with MCP servers.

**Trigger:**

*   **Task:** Use the `jules-cli` to interact with the `httpx` MCP server to get information about a website.
*   **Command:**
    ```bash
    jules-cli roo-code --mcp httpx --prompt "Get information about the website https://google.com"
    ```
*   **Expected Outcome:** Information about the website is printed to the console.

### 3.3 Codebase Indexing and Semantic Search

**Objective:** Learn how to index your codebase and perform semantic search.

**Trigger:**

*   **Task:** Use the `jules-cli` to index your codebase and then perform a semantic search to find all functions related to "authentication".
*   **Command:**
    1.  Index your codebase:
        ```bash
        jules-cli roo-code --index .
        ```
    2.  Perform a semantic search:
        ```bash
        jules-cli roo-code --search "functions related to authentication"
        ```
*   **Expected Outcome:** A list of functions related to "authentication" is printed to the console.

### 3.4 Browser Automation and Web Interaction

**Objective:** Learn how to automate browser interactions with Roo Code.

**Trigger:**

*   **Task:** Use the `jules-cli` to open a browser, navigate to Google, and search for "Roo Code".
*   **Command:**
    ```bash
    jules-cli roo-code --browse "https://google.com" --prompt "Search for 'Roo Code'"
    ```
*   **Expected Outcome:** A browser window is opened, and a search for "Roo Code" is performed.

### 3.5 Multi-file Refactoring and Testing Workflows

**Objective:** Learn how to perform multi-file refactoring and run tests with Roo Code.

**Trigger:**

*   **Task:** Use the `jules-cli` to refactor a function that is used in multiple files and then run the tests to ensure that the refactoring did not break anything.
*   **Command:**
    ```bash
    jules-cli roo-code --mode "Code Mode" --prompt "Refactor the function 'get_user' to 'find_user' in all files in the project. After the refactoring is complete, run the tests."
    ```
*   **Expected Outcome:** The function is refactored in all files, and the tests are run.

## Module 4: Real-World Applications

This module provides real-world case studies and workflow patterns.

### 4.1 Case Studies

**Objective:** Apply your Roo Code skills to real-world scenarios.

**Trigger:**

*   **Task:** Choose a project from your own GitHub account and use Roo Code to complete a task. For example, you could add a new feature, fix a bug, or improve the documentation.
*   **Command:** Use the `jules-cli` with the appropriate Roo Code modes and prompts to complete the task.
*   **Expected Outcome:** The task is completed successfully.

### 4.2 Workflow Patterns

**Objective:** Learn how to use Roo Code in your daily development workflow.

**Trigger:**

*   **Task:** Integrate Roo Code into your daily development workflow for one week. Use it for all your coding tasks, including planning, writing code, debugging, and testing.
*   **Command:** Use the `jules-cli` with the appropriate Roo Code modes and prompts to complete your daily tasks.
*   **Expected Outcome:** You are able to use Roo Code effectively in your daily development workflow.

## Module 5: Conclusion and Next Steps

This module summarizes the key takeaways and suggests next steps for continued learning.

### 5.1 Key Takeaways

*   Roo Code is a powerful AI-powered VS Code extension that can help you write, debug, and deploy software more effectively.
*   The `jules-cli` provides a command-line interface for Roo Code, allowing you to integrate it into your existing workflows.
*   Roo Code has five modes: "Code Mode", "Architect Mode", "Ask Mode", "Debug Mode", and "Orchestrator Mode".
*   Roo Code can be configured with different AI models to optimize for cost and performance.
*   Roo Code can be extended with custom modes and integrated with MCP servers.

### 5.2 Next Steps

*   **Join the Community:** Connect with other Roo Code users on Discord, Reddit, and GitHub.
*   **Contribute to the Project:** Roo Code is an open-source project. Contribute to the project by reporting bugs, suggesting new features, or submitting pull requests.
*   **Explore the Documentation:** The Roo Code documentation is a great resource for learning more about the advanced features of Roo Code.
