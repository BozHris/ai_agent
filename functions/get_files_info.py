import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path=os.path.join(working_directory, directory)
    absolute_path_working_dir=os.path.abspath(working_directory)
    absolute_path_full=os.path.abspath(full_path)
    
    if not  absolute_path_full.startswith(absolute_path_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    files=os.listdir(full_path)
    messages=[]
    for temp_file in files: 
        try:
            message= f"-{temp_file}: file_size={os.path.getsize(os.path.join(full_path,temp_file))} bytes, is_dir={os.path.isdir(os.path.join(full_path,temp_file))}"
        except Exception as e:
            return f"Error: {e}"
        else:
            messages.append(message)
        
    return "\n".join(messages)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions_info = types.Tool(
    function_declarations=[schema_get_files_info],
)



