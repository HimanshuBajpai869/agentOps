# AgentOps Platform

## Overview

AgentOps is a lightweight platform to standardize how agents are registered, versioned, deployed, and rolled back.

It replaces fragmented, team-specific workflows with a single unified system:

~~~
Register Agent → Version Agent → Deploy Agent → Rollback Agent
~~~

## Problem

Today, deploying agents is inconsistent and repetitive across teams:

~~~
Agent Code → Docker Image → Helm Chart → Kubernetes → Monitoring
~~~

Each team rebuilds this pipeline independently, leading to duplication, drift, and operational overhead.

## Goals
- Provide a central Agent Registry
- Enable consistent versioning of agents
- Support simple deployments and rollbacks
- Reduce infrastructure duplication across teams

## Operational Functionalities

### Functional

- Agent Registry
~~~
POST /agents – Register a new agent
POST /{agent_id}/activate/{version_id} - Activate a Agent Version
POST /{agent_id}/run - Send a prompt to the activated agent for a response.
GET /agents – List agents
GET /{agent_id}/runs - History of all the runs for the agent.
~~~

- Agent Versioning
~~~
POST /agents/{agent}/versions – Create a new version
GET /agents/{agent}/versions – List versions
~~~

- Deployments
~~~
POST /deployments – Deploy an agent version
GET /deployments – List deployments
~~~

- Rollback
~~~
POST /rollback – Roll back to a previous version
~~~

### Non-Functional Requirements

- Simplicity: Single binary-style deployment model
- Open Source Friendly: Runs locally via Docker Compose
- No cloud dependency: Works without AWS or managed services
- Kubernetes Native (future): Will evolve toward an AgentDeployment CRD

## Tech Stack

- Backend: FastAPI
- Language: Python 3.11
- Database: PostgreSQL 16
- ORM: SQLAlchemy 2.0
- Migrations: Alembic
- Package Manager: uv
- Deployment: Docker Compose (initially)

## Helpful Commands (TBD)
uv run python -m app.init_db

docker ps
docker exec -it 439f659d282f psql -U agentOps
DROP TABLE IF EXISTS agent_versions CASCADE;
DROP TABLE IF EXISTS agents CASCADE;

lsof -i :8000
kill -9 21474
