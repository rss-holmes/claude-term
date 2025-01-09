# Claude Terminal

A terminal-based tool for interacting with Claude AI, featuring project-based contexts and system prompts.

## Features
- Interactive conversations with Claude
- Project management with custom system prompts
- File context support for projects
- Rich terminal interface

## Prerequisites
- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/claude-term.git
cd claude-term
```

2. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Create a `.env` file with your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the tool:
```bash
python main.py
```

### Project Commands
- Create a new project: `python main.py project create --project-name=<project_name>` or `python main.py project create <project_name>`
- List projects: `python main.py list-projects`
- Add files to project: `python main.py project add-file --project-name=<project_name> --file-path=<file_path>` or `python main.py project add-file <project_name> <file_path>`
- Set system prompt: `python main.py set-prompt --project-name=<project_name> --prompt-file=<prompt_file>` or `python main.py set-prompt <project_name> <prompt_file>`

### Chat Commands
- Start chat (no project): `python main.py chat`
- Start chat with project: `python main.py chat --project-name=<project_name>`

## Development

The project uses uv for dependency management. To update dependencies:
```bash
uv pip compile pyproject.toml -o requirements.txt
``` 