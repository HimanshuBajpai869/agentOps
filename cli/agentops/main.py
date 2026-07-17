import typer

from agentops.commands.agent import app as agent_app
from agentops.commands.server import app as server_app

app = typer.Typer()

app.add_typer(
    agent_app,
    name="agent",
)

app.add_typer(
    server_app,
    name="server",
)

if __name__ == "__main__":
    app()
