import subprocess

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types
from rich.console import Console

from agent_ops_cockpit.ops.git_portal import GitPortal

console = Console()

def run_shell_command(cmd: str, dir: str = ".") -> dict:
    """Executes a shell command in the given directory and returns the output."""
    try:
        result = subprocess.run(cmd, cwd=dir, shell=True, capture_output=True, text=True, check=True)
        return {"status": "success", "stdout": result.stdout[:2000], "stderr": result.stderr[:2000]}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "stdout": e.stdout[:2000], "stderr": e.stderr[:2000], "exit_code": e.returncode}

def read_file(path: str) -> dict:
    """Reads the contents of a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {"status": "success", "content": f.read()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def write_file(path: str, content: str) -> dict:
    """Writes the given content completely overwriting the file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def fetch_url(url: str) -> dict:
    """Fetches text content from a public URL."""
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
             text = response.read().decode('utf-8')
             return {"status": "success", "content": text[:10000]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

upgrader_agent = Agent(
    name="AutonomousUpgrader",
    model="gemini-2.0-flash",
    instruction='''You are the Cockpit Autonomous Upgrader, an elite Enterprise Architect.
Your task is to modernize the specified repository based on the provided engineering docs.
Step 1: Read the engineering docs using `fetch_url`.
Step 2: Investigate the local repository using `run_shell_command` (e.g., `ls -R`, `cat requirements.txt`) and `read_file`.
Step 3: Refactor the code by completely rewriting files with `write_file` to adhere exactly to the new standards.
Step 4: Verify your changes by running `run_shell_command` against the codebase tests or linters.
Do NOT ask the user for permission. Just do the refactor autonomously and provide a detailed markdown summary of all modifications at the end.
''',
    tools=[run_shell_command, read_file, write_file, fetch_url],
)

async def run_autonomous_upgrade(path: str, docs_url: str):
    import time
    console.print("🚀 [bold blue]Cockpit Autonomous Upgrader Initializing...[/bold blue]")
    console.print(f"📡 Target Path: [cyan]{path}[/cyan] | Standards Docs: [cyan]{docs_url}[/cyan]")
    
    # 1. Shadow Sandbox (Safety via Git)
    portal = GitPortal(path)
    branch_name = f"cockpit-upgrade-{int(time.time())}"
    console.print("🛡️  [bold yellow]Creating Git Sandbox...[/bold yellow]")
    if portal.repo:
        portal.create_fix_branch(branch_name)
        console.print(f"   [dim]Switched to branch: {branch_name}[/dim]")
    else:
        console.print("⚠️  [red]Failed to initialize Git Sandbox. Proceeding on current branch.[/red]")
        branch_name = "default_session"
    
    # 2. Run the ADK Agent
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="cockpit", user_id="cli_user", session_id=branch_name
    )
    runner = Runner(agent=upgrader_agent, app_name="cockpit", session_service=session_service)
    
    prompt = f"Begin the upgrade on repository path: {path}. Extract the new architectural standards from this URL: {docs_url} and apply them."
    console.print("🤖 [bold green]Agent Dispatched![/bold green] Working autonomously in the background...")
    console.print("="*60)
    
    async for event in runner.run_async(
        user_id="cli_user",
        session_id=branch_name,
        new_message=genai_types.Content(role="user", parts=[genai_types.Part.from_text(text=prompt)])
    ):
        if hasattr(event, "is_tool_call") and event.is_tool_call():
             console.print(f"   [dim]🔧 Agent invoked tool:[/] [cyan]{event.tool_name}[/cyan]")
        elif hasattr(event, "is_final_response") and event.is_final_response():
             console.print("\n✨ [bold magenta]Agent Upgrade Summary & Changelog:[/bold magenta]")
             console.print(event.content.parts[0].text)

    # 3. Finalization
    console.print("="*60)
    console.print("✅ [bold green]Autonomous Refactoring Complete![/bold green]")
    if portal.repo:
        console.print(f"👉 Review the differential in Git: [white]git diff main..{branch_name}[/white]")
        console.print(f"👉 To adopt changes, merge the branch: [white]git checkout main && git merge {branch_name}[/white]")
