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

### Pre-requisites

1. Install colima following the doc - https://colima.run/docs/installation/
~~~
brew install colima
~~~

2. Start Colima

~~~
colima start
~~~

### Setup Infrastructure

1. Start Services needed for the app using docker compose

~~~
docker compose up -d
~~~

2. Verify if infrastructure needed is up

~~~
docker ps
~~~

You should see the details of container. These can be used to connect with the container for debugging like below

~~~
docker exec -it 439f659d282f psql -U agentOps
DROP TABLE IF EXISTS agent_versions CASCADE;
DROP TABLE IF EXISTS agents CASCADE;
~~~

### Run Application

Note - We are using uv for dependencies management. You can also activate a uv environment to run the next set of commands

1. Setup Tables in Postgres-

~~~
uv run python -m app.init_db
~~~

Swagger UI with the documentation will be available - http://localhost:8000/docs 

2. Start the API Server using unicorn

~~~
uv run uvicorn app.main:app --reload
~~~

3. Setup Open Source LLM using Ollama

~~~
brew install ollama
~~~

~~~
ollama serve
~~~

~~~
ollama pull tinyllama
~~~

4. Spin up UI for the Application

- Install Node JS

~~~
brew install node
~~~

- Spin Up UI with below command -

~~~
npm run dev
~~~

## Helpful Commands 
lsof -i :8000
kill -9 21474
