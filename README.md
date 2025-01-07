# Claude Terminal

A terminal-based tool for interacting with Claude AI, featuring project-based contexts and system prompts.

## Features
- Interactive conversations with Claude
- Project management with custom system prompts
- File context support for projects
- Rich terminal interface

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run the tool:
```bash
python main.py
```

### Project Commands
- Create a new project: `python main.py project create <name>`
- List projects: `python main.py project list`
- Add files to project: `python main.py project add-file <project> <file>`
- Set system prompt: `python main.py project set-prompt <project> <prompt_file>`

### Chat Commands
- Start chat (no project): `python main.py chat`
- Start chat with project: `python main.py chat --project <name>` 