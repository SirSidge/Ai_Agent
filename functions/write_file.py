import os

from google.genai import types

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
        return f'Successfully wrote \'{content}\' to "{file_path}" ({len(content)} characters written)'
    except IOError as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Checks if the directory path exists and creates it if not. Then opens the specified file and writes/overwrites the content of that file, then providing feedback once completed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The specific file, relative to the working directory, that is created and/or written into.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text that should be written into the specified file."
            )
        },
        required=["file_path", "content"],
    ),
)