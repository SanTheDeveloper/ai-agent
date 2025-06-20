import os
from config import MAX_CHARS  # Import maximum character limit from configuration


def get_file_content(working_directory, file_path):
    """
    Safely reads and returns the content of a file within a restricted working directory.

    Args:
        working_directory (str): The base directory where file access is permitted
        file_path (str): Relative path to the target file from working_directory

    Returns:
        str: File contents (truncated if exceeding MAX_CHARS) or error message
    """

    # Convert both paths to absolute paths for reliable comparison
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Verify requested file is within permitted directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Validate the path points to an existing regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Open file in read mode (context manager ensures proper file closure)
        with open(abs_file_path, "r") as f:
            # Read content up to MAX_CHARS limit
            content = f.read(MAX_CHARS)

            # Check if content reached MAX_CHARS (potential truncation)
            if len(content) == MAX_CHARS:
                # Append truncation notice if file was actually larger
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        # Handle any file reading errors (permissions, encoding, etc.)
        return f'Error reading file "{file_path}": {e}'
