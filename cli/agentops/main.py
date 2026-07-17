import typer

from agentops.commands.agent import app as agent_app

app = typer.Typer()

app.add_typer(
    agent_app,
    name="agent",
)

if __name__ == "__main__":
    app()
