from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    result = ""
    function_name = ""
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    if function_call_part.name == "get_file_content":
        result = get_file_content("./calculator", function_call_part.args["file_path"])
        function_name = "get_file_content"
    if function_call_part.name == "get_files_info":
        if function_call_part.args:
            result = get_files_info("./calculator", function_call_part.args["directory"])
        else:
            result = get_files_info("./calculator")
        function_name = "get_files_info"
    if function_call_part.name == "run_python_file":
        result = run_python_file("./calculator", function_call_part.args["file_path"], function_call_part.args["args"])
        function_name = "run_python_file"
    if function_call_part.name == "write_file":
        result = write_file("./calculator", function_call_part.args["file_path"], function_call_part.args["content"])
        function_name = "write_file"
    if not (function_call_part.name == "get_file_content" or function_call_part.name == "get_files_info" or function_call_part.name == "run_python_file" or function_call_part.name == "write_file"):
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    result={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )