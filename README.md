# The Clean Code Bot

Python CLI that reads a source file, sends it to **Groq Cloud** for inference, and prints (or writes) a refactored version that emphasizes **object-oriented design**, **SOLID** principles, consistent indentation, and language-appropriate documentation (docstrings, JSDoc, etc.).
#### This code is supposed to be a result of a over engineered promp, and it didn't follow the industry quality standards neither process like planning,  development, testing, requirement refinement 

## Requirements

- Python 3.9+
- A [Groq](https://console.groq.com/) API key (free tier supported)

## Install

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

Set your API key in the environment:

```bash
export GROQ_API_KEY="gsk_..."   # use your key from Groq Console
```

Optional: copy `.env.example` to `.env` and load it with your shell or a tool of your choice; the CLI reads **`GROQ_API_KEY` from the environment** only (it does not load `.env` automatically).

## Usage

```bash
clean-code-bot path/to/module.py
clean-code-bot path/to/app.js -o path/to/refactored.js
clean-code-bot src/foo.py --model llama-3.1-8b-instant
```

- **`--output` / `-o`**: write the result to a file instead of stdout.
- **`--model` / `-m`**: Groq model id (default: `llama-3.3-70b-versatile`).
- **`--max-bytes`**: override the maximum source file size (default 256 KB).

Run as a module without installing:

```bash
pip install -r requirements.txt   # if you prefer requirements over editable install
python -m clean_code_bot --help
```

For editable install, `pip install -e .` is enough (dependencies come from `pyproject.toml`).

## Dependencies

Declared in `pyproject.toml`:

- **click** — CLI
- **groq** — Groq Cloud OpenAI-compatible API client

## Security notes

Input is validated (size, UTF-8, no null bytes, no delimiter collisions) and wrapped in explicit `<<<SOURCE_BEGIN>>>` / `<<<SOURCE_END>>>` markers. The reusable **chain-of-thought prompt template** (`clean_code_bot/prompt_template.py`) instructs the model to treat that region as untrusted data and not to follow embedded instructions. This reduces prompt-injection risk but is not a substitute for not running untrusted code.

## Project layout

- `clean_code_bot/cli.py` — Click entrypoint
- `clean_code_bot/prompt_template.py` — reusable CoT prompt template
- `clean_code_bot/sanitization.py` — validation and safe wrapping
- `clean_code_bot/groq_client.py` — Groq API call and fenced-code extraction

## License

Use and modify as needed for your organization.
