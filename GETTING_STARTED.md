# Getting Started with the PAI CLI

This guide will walk you through the process of installing and using the PAI CLI, a powerful tool for interacting with the Personal AI Infrastructure.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/valentinuuiuiu/Personal_AI_Infrastructure.git
    cd Personal_AI_Infrastructure
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    *   Copy the `.env.example` file to `.env.local`:
        ```bash
        cp piata-ai-new/.env.example piata-ai-new/.env.local
        ```
    *   Open `piata-ai-new/.env.local` and add your OpenRouter API key:
        ```
        OPENROUTER_API_KEY=your-api-key-here
        ```

## Usage

The PAI CLI is a versatile tool that allows you to interact with the PAI in a variety of ways. Here are a few examples:

*   **Ask a question:**
    ```bash
    python3 pai/pai.py ask "What is the capital of France?"
    ```

*   **Run an agent:**
    ```bash
    python3 pai/pai.py run_agent researcher "What is the airspeed velocity of an unladen swallow?"
    ```

*   **Extract wisdom from a URL:**
    ```bash
    python3 pai/pai.py extract_wisdom --url https://www.google.com
    ```

## The "Fabric" Web Terminal

The "fabric" web terminal provides a user-friendly interface for interacting with the PAI CLI. To use it, simply start the `piata-ai-new` Next.js application and navigate to the home page.

1.  **Start the Next.js application:**
    ```bash
    cd piata-ai-new
    npm install
    npm run dev
    ```

2.  **Open your browser to `http://localhost:3000`** and you will see the "fabric" terminal. You can then use the `ask`, `run_agent`, and `extract_wisdom` commands directly in the terminal.
