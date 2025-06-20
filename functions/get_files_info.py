import os


def get_files_info(working_directory, directory=None):
    """
    Get information about files in a specified directory, with safety checks to prevent
    accessing files outside the permitted working directory.

    Args:
        working_directory (str): The base directory where operations are permitted
        directory (str, optional): The target directory to list. Defaults to None (working_directory).

    Returns:
        str: Formatted string with file info or error message prefixed with 'Error:'
    """

    # Convert working directory to absolute path for reliable comparison
    abs_working_dir = os.path.abspath(working_directory)

    # Set default target directory (same as working directory if none specified)
    target_dir = abs_working_dir

    # If a specific directory was requested, resolve its absolute path
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))

    # Security check: ensure target directory is within permitted working directory
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Verify the target path is actually a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        # Initialize list to store file information strings
        files_info = []

        # List all entries in the target directory
        for filename in os.listdir(target_dir):
            # Get full path of the current file/directory
            filepath = os.path.join(target_dir, filename)

            # Determine if entry is a directory and get its size
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(
                filepath
            )  # Note: directory sizes may vary by OS

            # Format the entry information and add to our list
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        # Combine all entries into a single string with newline separators
        return "\n".join(files_info)

    except Exception as e:
        # Catch any unexpected errors and return them in a standardized format
        return f"Error listing files: {e}"
