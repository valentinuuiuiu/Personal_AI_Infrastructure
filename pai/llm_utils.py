import os
from openai import OpenAI

# Initialize the OpenAI client
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    # We won't exit here, as this module might be imported in environments
    # where the API key is not required. The calling code should handle this.
    print("Warning: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
    client = None
else:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def call_llm(messages: list, stream: bool = False):
    """
    Sends a list of messages to the LLM.
    If stream is True, yields response chunks.
    Otherwise, returns the complete response content.
    """
    if not client:
        error_message = "OpenAI client is not initialized. Please set the OPENROUTER_API_KEY environment variable."
        if stream:
            yield error_message
        else:
            return error_message

    try:
        completion = client.chat.completions.create(
            model="minimax/minimax-m2:free",
            messages=messages,
            temperature=0.1,
            stream=stream,
        )
        if stream:
            def stream_generator():
                for chunk in completion:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
            return stream_generator()
        else:
            return completion.choices[0].message.content
    except Exception as e:
        error_message = f"An error occurred: {e}"
        if stream:
            yield error_message
        else:
            return error_message
