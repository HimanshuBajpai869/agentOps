from app.models.agent_run import AgentRun


class AgentRunner:
    @staticmethod
    def run(db, agent, version):

        result = AgentRunner.prompt_agent(agent, version)

        run = AgentRun(
            agent_id=agent.id,
            version_id=version.id,
            input_prompt=version.prompt,
            output=result["response"],
        )

        db.add(run)
        db.commit()
        db.refresh(run)

        return {
            "run_id": run.id,
            "agent_id": agent.id,
            "version_id": version.id,
            "response": result["response"],
        }

    @staticmethod
    def prompt_agent(agent, version):

        return {
            "agent_id": str(agent.id),
            "version": version.version,
            "prompt_used": version.prompt,
            "response": f"[MOCK RESPONSE] executed prompt: {version.prompt}",
        }
