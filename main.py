# Import standard libraries
import sys
import os

# Google Gemini SDK imports
from google import genai
from google.genai import types

# Load environment variables from .env file
from dotenv import load_dotenv


def generate_content(client, messages, verbose, system_prompt=None):
    """
    Generates and prints a response from the Gemini model with optional system prompt.

    Args:
        client (genai.Client): Authenticated Gemini client
        messages (list): List of Content objects
        verbose (bool): Print token usage details
        system_prompt (str): System instructions for the AI
    """
    # Prepare config with system prompt if provided
    config = (
        types.GenerateContentConfig(system_instruction=system_prompt)
        if system_prompt
        else None
    )

    # Get response from Gemini model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages, config=config
    )

    # Print token usage if verbose mode is enabled
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Print the generated response
    print("Response:")
    print(response.text)


def main():
    """Main function to handle user input and control flow."""
    load_dotenv()  # Load environment variables

    # Check if --verbose flag is present
    verbose = "--verbose" in sys.argv

    # Filter out flags to get only the prompt-related arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    # Hardcoded system prompt as per assignment
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    # Exit with usage message if no prompt provided
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Retrieve the Gemini API key from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        sys.exit(1)

    # Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    # Join all prompt arguments into a single string
    user_prompt = " ".join(args)

    # Print the prompt if verbose mode is enabled
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        print(f"System prompt: {system_prompt}\n")

    # Create conversation history
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Generate response with system prompt
    generate_content(client, messages, verbose, system_prompt)


if __name__ == "__main__":
    main()
