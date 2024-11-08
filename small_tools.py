def get_file_as_string(file_path):
    """Reads the contents of a file and returns it as a string."""
    with open(file_path, 'r') as file:
        return file.read()