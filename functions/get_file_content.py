import os

from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_wd = os.path.realpath(working_directory)
    abs_path = os.path.realpath(os.path.join(abs_wd, file_path))
    if not (abs_path == abs_wd or abs_path.startswith(abs_wd + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_path, "r") as f:
            data = f.read(MAX_CHARS + 1)
    except Exception as e:
        return f'Error: {e}'
    if len(data) > MAX_CHARS:
        data = data[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return data