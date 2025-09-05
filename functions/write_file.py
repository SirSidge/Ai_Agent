import os

def write_file(working_directory, file_path, content):
    abs_wd = os.path.realpath(working_directory)
    abs_path = os.path.realpath(os.path.join(abs_wd, file_path))
    if not (abs_path == abs_wd or abs_path.startswith(abs_wd + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    dirpath = os.path.dirname(abs_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    try:
        with open(abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except IOError as e:
        return f"Error: {e}"