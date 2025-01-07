import os
import typer
import yaml
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown
from anthropic import Anthropic
from dotenv import load_dotenv

# Initialize typer app and console
app = typer.Typer()
console = Console()

# Load environment variables
load_dotenv()

# Constants
PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

class Project:
    def __init__(self, name: str):
        self.name = name
        self.path = PROJECTS_DIR / name
        self.path.mkdir(exist_ok=True)
        self.config_path = self.path / "config.yaml"
        self.files_dir = self.path / "files"
        self.files_dir.mkdir(exist_ok=True)
        
        if self.config_path.exists():
            with open(self.config_path) as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {
                "system_prompt": "",
                "files": []
            }
            self._save_config()
    
    def _save_config(self):
        with open(self.config_path, "w") as f:
            yaml.dump(self.config, f)
    
    def set_system_prompt(self, prompt: str):
        self.config["system_prompt"] = prompt
        self._save_config()
    
    def add_file(self, file_path: str):
        if file_path not in self.config["files"]:
            self.config["files"].append(file_path)
            self._save_config()
    
    def get_context(self) -> str:
        context = []
        if self.config["system_prompt"]:
            context.append(self.config["system_prompt"])
        
        for file_path in self.config["files"]:
            full_path = self.files_dir / file_path
            if full_path.exists():
                context.append(f"Content of {file_path}:")
                context.append(full_path.read_text())
        
        return "\n\n".join(context)

# Project commands
@app.command()
def create(name: str):
    """Create a new project"""
    project = Project(name)
    console.print(f"Created project: {name}")

@app.command()
def list_projects():
    """List all projects"""
    projects = [p.name for p in PROJECTS_DIR.iterdir() if p.is_dir()]
    if not projects:
        console.print("No projects found")
        return
    console.print("Projects:")
    for project in projects:
        console.print(f"- {project}")

@app.command()
def add_file(project_name: str, file_path: str):
    """Add a file to a project"""
    project = Project(project_name)
    
    # Copy file to project directory
    source = Path(file_path)
    if not source.exists():
        console.print(f"Error: File {file_path} not found")
        return
    
    dest = project.files_dir / source.name
    dest.write_text(source.read_text())
    project.add_file(source.name)
    console.print(f"Added file {source.name} to project {project_name}")

@app.command()
def set_prompt(project_name: str, prompt_file: str):
    """Set system prompt for a project"""
    project = Project(project_name)
    prompt_path = Path(prompt_file)
    
    if not prompt_path.exists():
        console.print(f"Error: File {prompt_file} not found")
        return
    
    prompt = prompt_path.read_text()
    project.set_system_prompt(prompt)
    console.print(f"Updated system prompt for project {project_name}")

# Chat command
@app.command()
def chat(project_name: Optional[str] = None):
    """Start a chat session with Claude"""
    anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    if not anthropic.api_key:
        console.print("Error: ANTHROPIC_API_KEY not found in .env file")
        return
    
    system = None
    if project_name:
        project = Project(project_name)
        system = project.get_context()
    
    messages = []
    console.print("Starting chat with Claude (type 'exit' to end)")
    console.print("----------------------------------------")
    
    while True:
        user_input = Prompt.ask("\n[bold green]You[/bold green]")
        
        if user_input.lower() == "exit":
            break
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            console.print("\nClaude:", style="bold blue")
            
            # Initialize variables for streaming
            current_message = []
            
            # Stream the response
            with anthropic.messages.stream(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=messages,
                system=system,
                temperature=0.7,
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        # Get the new text and append to message
                        new_text = chunk.delta.text
                        current_message.append(new_text)
                        # Print just the new chunk
                        console.print(new_text, end="", markup=False)
            
            # Print a newline after streaming is complete
            console.print()
            
            # Add the complete message to the history
            complete_message = "".join(current_message)
            messages.append({"role": "assistant", "content": complete_message})
            
        except Exception as e:
            console.print(f"Error: {str(e)}", style="bold red")

if __name__ == "__main__":
    app() 