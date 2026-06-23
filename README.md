# agentOps

uv run python -m app.init_db

docker ps
docker exec -it 439f659d282f psql -U agentOps
DROP TABLE IF EXISTS agent_versions CASCADE;
DROP TABLE IF EXISTS agents CASCADE;

lsof -i :8000
kill -9 21474