import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path=os.path.join(working_directory, file_path)
    absolute_path_working_dir=os.path.abspath(working_directory)
    absolute_path_full=os.path.abspath(full_path)
    
    if not  absolute_path_full.startswith(absolute_path_working_dir):   
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        cmd=["python", full_path]+args
        completed_process = subprocess.run(cmd,capture_output=True,text=True,timeout=30,check=True) 
    except Exception as e:
        return f"Error: executing Python file: {e}"
    else:
        if completed_process.returncode==0:
            return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}\nNo output produced"
        return f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}\nProcess exited with code {completed_process.returncode}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run , relative to the working directory. If not provided, follow program procedure.",
            ),
        },
    ),
)


available_functions_run = types.Tool(
    function_declarations=[schema_run_python_file],
)