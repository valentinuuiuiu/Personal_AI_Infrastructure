
import sys

def get_best_free_model(prompt: str = None) -> str:
    """
    Selects the best free model available on OpenRouter for a given prompt.

    This function acts as a routing agent. Its primary goal is to choose the
    most capable and cost-effective model for the user's task. The logic
    can be expanded to analyze the prompt and route it to specialized models.

    Future enhancements:
    - Analyze the prompt to detect intent (e.g., coding, writing, translation).
    - Maintain a dynamic list of preferred free models.
    - Route to specialized models (e.g., code generation models for coding tasks).
    - Implement a fallback mechanism if a preferred model is unavailable.

    Args:
        prompt: The user prompt (reserved for future routing logic).

    Returns:
        The identifier of the selected language model.
    """
    # For now, we use a reliable, general-purpose model that is widely available
    # and has a good performance-to-cost ratio on the free tier.
    return "mistralai/mistral-7b-instruct"

if __name__ == "__main__":
    # If the script is called directly, it prints the model name.
    # This allows it to be called as a subprocess from other skills.
    # The first argument (the script name itself) is ignored.
    user_prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    selected_model = get_best_free_model(user_prompt)
    print(selected_model)
