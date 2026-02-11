
A small Python coding agent powered by Google Gemini that can inspect files, read file contents, write files, and run Python scripts inside a constrained working directory.
 
 ## What this project does
 
 The agent:
 
 - accepts a natural-language prompt from the command line,
 - sends the request to Gemini (`gemini-2.5-flash`),
 - executes tool/function calls returned by the model,
 - feeds tool outputs back to the model in a loop,
 - stops when the model returns a final text response.
 
 The default sandboxed target directory is:
 
 - `./calculator`
 
 ## Project structure
 
 - `main.py` – CLI entrypoint and model/tool orchestration loop.
 - `prompts.py` – system prompt for tool-use behavior.
 - `config.py` – shared config (`max_chars` for file reads).
 - `functions/` – tool implementations and Gemini function schemas:
   - `get_files_info.py`
   - `get_file_content.py`
   - `write_file.py`
   - `run_python_file.py`
 - `calculator/` – sample target codebase used as the working directory.
 - `test_*.py`, `tests.py` – script-style checks for tool behavior.
 
 ## Requirements
 
 - Python 3.12 
 - A Gemini API key
 
 Dependencies (from `pyproject.toml`):
 
 - `google-genai==1.12.1`
 - `python-dotenv==1.1.0`
 
 ## Setup
 
 1. Create and activate a virtual environment.
 2. Install dependencies.
 3. Provide your API key as an environment variable.
 
 Example:
 
 ```bash
 python -m venv .venv
 source .venv/bin/activate
 pip install -e .
 export GEMINI_API_KEY="your_api_key_here"
 ```
 
 You can also place the key in a `.env` file because `main.py` calls `load_dotenv()`.
 
 ## Usage
 
 Run the agent with a prompt:
 
 ```bash
 python main.py "list files in the project"
 ```
 
 Verbose mode:
 
 ```bash
 python main.py "read calculator/main.py and summarize it" --verbose
 ```
 
 If you run without a prompt, the program exits with a helpful message.
 
 ## Tool behavior and safety
 
 Each tool is restricted to the configured `working_directory` (`./calculator` by default):
 
 - path traversal outside the working directory is rejected,
 - non-existent or invalid paths return explicit error strings,
 - `get_file_content` truncates very long files to `max_chars` (default 10,000),
 - `run_python_file` only runs `.py` files and includes a timeout.
 
 ## Running checks
 
 This repository uses script-style tests. Run them directly:
 
 ```bash
 python tests.py
 python test_get_file_content.py
 python test_write_file.py
 python test_run_python_file.py
 ```
 
 You can also run the sample calculator checks:
 
 ```bash
 python calculator/tests.py
 ```
 
 ## Notes
 
 - The current implementation keeps tool-call outputs in-memory and iterates up to 20 rounds.
 - `main.py` currently targets `gemini-2.5-flash` explicitly.


