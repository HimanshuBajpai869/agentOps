from app.db.base import Base
from app.db.database import engine

import app.models.agent
import app.models.agent_version

Base.metadata.create_all(bind=engine)

print("tables created")
