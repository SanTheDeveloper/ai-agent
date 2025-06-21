import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python file within a secure working directory with timeout protection.

    Args:
        working_directory (str): The base directory where execution is permitted
        file_path (str): Relative path to the Python file from working_directory
        args (list, optional): Additional command line arguments for the script

    Returns:
        str: Formatted execution output or error message. Contains:
            - STDOUT content if any
            - STDERR content if any
            - Process exit code if non-zero
            - Error messages if execution fails
    """

    # Convert paths to absolute paths for reliable security checks
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security Check 1: Prevent directory traversal
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Security Check 2: Verify file exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    # Security Check 3: Ensure only Python files can execute
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Prepare the execution command
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)  # Add any additional arguments

        # Execute the Python file with security constraints:
        # - capture_output: Redirects stdout/stderr for parsing
        # - text: Returns output as strings (not bytes)
        # - timeout: Prevents infinite execution (30 seconds)
        # - cwd: Sets the working directory for execution
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )

        # Format the output components
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")  # Standard output
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")  # Error output

        # Add return code if execution failed
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        # Combine all output or return default message
        return "\n".join(output) if output else "No output produced."

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
