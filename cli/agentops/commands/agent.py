import typer

from rich import print

from agentops.client import AgentOpsClient

app = typer.Typer()

client = AgentOpsClient()


@app.command()
def create():

    name = typer.prompt("Agent Name")

    description = typer.prompt("Description")

    owner = typer.prompt("Owner")

    agent = client.create_agent(
        name=name,
        description=description,
        owner=owner,
    )

    print(agent)


@app.command()
def list():

    agents = client.list_agents()

    print(agents)
