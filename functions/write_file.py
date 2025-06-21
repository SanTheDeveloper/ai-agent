import os


def write_file(working_directory, file_path, content):
    """
    Safely writes content to a file within a restricted working directory.

    Args:
        working_directory (str): The base directory where file operations are permitted
        file_path (str): Relative path to the target file from working_directory
        content (str): Content to be written to the file

    Returns:
        str: Success message with character count or error message prefixed with "Error:"
    """

    # Convert both paths to absolute paths for reliable comparison
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure target path is within permitted working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # If file doesn't exist, create parent directories first
    if not os.path.exists(abs_file_path):
        try:
            # Create all necessary parent directories (exist_ok prevents errors if dirs exist)
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    # Additional safety check: Verify path isn't an existing directory
    if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        # Open file in write mode (creates or truncates file)
        with open(abs_file_path, "w") as f:
            f.write(content)

        # Return success message with character count
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        # Handle any file writing errors (permissions, disk full, etc.)
        return f"Error: writing to file: {e}"
