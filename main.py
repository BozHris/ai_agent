import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, available_functions_info,get_files_info
from functions.get_file_content import schema_get_file_content, available_functions_content,get_file_content
from functions.write_file import schema_write_file,available_functions_write,write_file
from functions.run_python_file import schema_run_python_file,available_functions_run,run_python_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
working_directory = "./calculator"
TOOLS = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    try:
        function_name = function_call_part.name
        
        function_args = function_call_part.args
        
        func=TOOLS[function_name]
        
        function_result = func(working_directory, **function_args)
        
    except Exception: 
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )



def main():
    message = sys.argv[1:]
    if message == []:
        print("Please provide a message as a command line argument.")
        sys.exit(1)

    user_prompt = message[0]
    curr_verbose = "--verbose" in sys.argv

    list_to_use_later = []

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    for count in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[
                        available_functions_run,
                        available_functions_write,
                        available_functions_content,
                        available_functions_info,
                    ],
                    system_instruction=system_prompt,
                ),
            )
            candidates_propperty=response.candidates
            for candidate in candidates_propperty:
                messages.append(candidate.content)

            function_calls = response.function_calls
            if isinstance(function_calls, list):
                for i in function_calls:
                    result = call_function(i, verbose=curr_verbose)
                    list_to_use_later.append(result.parts[0])

                    if curr_verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    else:
                        print(result.parts[0].function_response.response)
                messages.append(types.Content(role="user", parts=list_to_use_later))

            if curr_verbose and getattr(response, "usage_metadata", None):
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        except Exception as e: 
            print(f"Error {e}")
            break
        else:
            if not response.function_calls and response.text:
                break
            else:
                count+=1


if __name__ == "__main__":
    main()






























    #code for forgotten lesson-disregard
    # user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=user_prompt,
    # )

    # if not response.usage_metadata:
    #     raise RuntimeError("Gemini API response appears to be malformed")

    # print("User prompt:", user_prompt)
    # print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    # print("Response tokens:", response.usage_metadata.candidates_token_count)
    # print("Response:")
    # print(response.text)
