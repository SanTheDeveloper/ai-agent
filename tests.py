# Import the function we want to test from our functions directory
from functions.get_file_content import get_file_content


def test():
    """
    Test function for get_file_content that verifies three scenarios:
    1. Reading a file in the working directory (main.py)
    2. Reading a file in a subdirectory (pkg/calculator.py)
    3. Attempting to read a file outside permitted directory (/bin/cat)
    """

    # Test Case 1: Read main.py from the working directory
    # Expected: Should return the file contents (possibly truncated)
    result = get_file_content("calculator", "main.py")
    print(result)  # Print the file contents or error message

    # Test Case 2: Read calculator.py from a subdirectory
    # Expected: Should return the file contents (possibly truncated)
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)  # Print the file contents or error message

    # Test Case 3: Attempt to read system file /bin/cat
    # Expected: Should return an error message since it's outside permitted directory
    result = get_file_content("calculator", "/bin/cat")
    print(result)  # Print the error message


if __name__ == "__main__":
    # Only execute the test function if this script is run directly
    # (not when imported as a module)
    test()
