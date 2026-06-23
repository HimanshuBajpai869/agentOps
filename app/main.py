from fastapi import FastAPI

from app.api.agent import router as agent_router
from app.api.agent_version import router as version_router

app = FastAPI(title="AgentOps")

app.include_router(agent_router)
app.include_router(version_router)
