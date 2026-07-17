import typer
import uvicorn

app = typer.Typer(invoke_without_command=True)


@app.callback()
def server(
    ctx: typer.Context,
    host: str = "0.0.0.0",
    port: int = 8000,
):
    """
    Start AgentOps backend.
    """

    if ctx.invoked_subcommand is not None:
        return

    print("🚀 Starting AgentOps Backend...")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
    )
