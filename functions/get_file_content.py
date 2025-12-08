from logging import config
import os
from config import max_chars
from google.genai import types

def get_file_content(working_directory,file_path):
    full_path=os.path.join(working_directory, file_path)
    absolute_path_working_dir=os.path.abspath(working_directory)
    absolute_path_full=os.path.abspath(full_path)
    
    if not  absolute_path_full.startswith(absolute_path_working_dir):   
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"' 
    

    try:
        with open(full_path,"r",encoding="utf-8") as f:
            get_file_content=f.read()
    except Exception as e:
        return f"Error: {e}"
    else:
            if len(get_file_content)>max_chars:
                return get_file_content[:max_chars]+f"\n[...File {file_path} truncated at {max_chars} characters]"
            else:
                return get_file_content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists file content in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path to list content from, relative to the working directory. If not provided, follow program procedure.",
            ),
        },
    ),
)


available_functions_content = types.Tool(
    function_declarations=[schema_get_file_content],
)