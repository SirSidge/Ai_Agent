import os

def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working, directory))
    contents_dir = f"Result for '{directory}' directory:" if directory != "." and directory is not None else f"Result for current directory:"
    if not os.path.abspath(target_path).startswith(abs_working):
        contents_dir += f'\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(target_path):
        contents_dir += f'\n    Error: "{directory}" is not a directory'
    else:
        contents = sorted(os.listdir(target_path))
        for item in contents:
            name = item
            file_size = os.path.getsize(os.path.abspath(os.path.join(working_directory, directory, item)))
            is_dir = os.path.isdir(os.path.abspath(os.path.join(working_directory, directory, item)))
            contents_dir += (f'\n - {name}: file_size={file_size} bytes, is_dir={is_dir}')
    return contents_dir