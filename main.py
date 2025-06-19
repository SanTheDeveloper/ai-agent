# Import necessary modules
import os
import sys  # Required for reading command line arguments
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Read the Gemini API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")

# Check if an API key was found; exit if not
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# Create the Gemini client
client = genai.Client(api_key=api_key)

# Check if a prompt was provided as a command line argument
if len(sys.argv) < 2:
    print("Error: No prompt provided.")
    print('Usage: python3 main.py "Your prompt here"')
    sys.exit(1)

# Get the prompt from the command line
prompt = sys.argv[1]

# Generate content using the Gemini model
content_obj = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=prompt,
)

# Print the generated response
print(content_obj.candidates[0].content.parts[0].text)

# Print token usage for transparency
print(f"Prompt tokens: {content_obj.usage_metadata.prompt_token_count}")
print(f"Response tokens: {content_obj.usage_metadata.candidates_token_count}")
