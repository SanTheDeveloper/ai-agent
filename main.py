# Import standard libraries
import sys  # For command-line arguments
import os  # For environment variable access

# Google Gemini SDK imports
from google import genai
from google.genai import types  # For structured content and part types

# Load environment variables from .env file
from dotenv import load_dotenv


def main():
    """
    Main function to handle user input and control flow.
    Supports optional --verbose flag for detailed output.
    """
    load_dotenv()  # Load environment variables

    # Check if --verbose flag is present
    verbose = "--verbose" in sys.argv

    # Filter out flags to get only the prompt-related arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

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

    # Create a list of Content objects (currently just one user message)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Generate response using the Gemini model
    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    """
    Generates and prints a response from the Gemini model.

    Args:
        client (genai.Client): Authenticated Gemini client
        messages (list): List of Content objects representing the conversation history
        verbose (bool): Whether to print token usage details or not
    """
    # Get response from Gemini model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # Optionally print token usage if verbose is enabled
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Always print the generated response
    print("Response:")
    print(response.text)


# Entry point of the program
if __name__ == "__main__":
    main()
