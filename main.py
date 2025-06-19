# Import standard library modules
import sys
import os

# Import Google Gemini SDK modules
from google import genai
from google.genai import types

# Import dotenv for environment variable loading
from dotenv import load_dotenv


def main():
    """
    Main function to handle command-line input and initiate the Gemini API interaction.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get command-line arguments (skip the script name)
    args = sys.argv[1:]

    # Check if the user provided a prompt
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # Join all parts of the command line argument in case of spaces
    user_prompt = " ".join(args)

    # Retrieve the Gemini API key from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")

    # Initialize the Gemini client with the provided API key
    client = genai.Client(api_key=api_key)

    # Create a message list containing the user's prompt as structured content
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Call the function to generate content using the Gemini model
    generate_content(client, messages)


def generate_content(client, messages):
    """
    Generates a response using the Gemini model based on the given messages.

    Args:
        client (genai.Client): The Gemini API client.
        messages (list): A list of types.Content objects representing the conversation history.
    """
    # Generate content using the Gemini model
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # Print the generated text from the response
    print("Response:")
    print(response.text)


# Entry point of the program
if __name__ == "__main__":
    main()
