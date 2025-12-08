import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path=os.path.join(working_directory, file_path)
    absolute_path_working_dir=os.path.abspath(working_directory)
    absolute_path_full=os.path.abspath(full_path)
    
    if not absolute_path_full.startswith(absolute_path_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    else:
        return f"Successfully wrote to {file_path} ({len(content)} characters written)"
    

schema_write_file=types.FunctionDeclaration(
    name="write_file",
    description="Write content to files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path where to write content, relative to the working directory. If not provided, follow program procedure.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file_path. If not provided, follow program procedure.",
            )
        },
    ),
)


available_functions_write = types.Tool(
    function_declarations=[schema_write_file],
)