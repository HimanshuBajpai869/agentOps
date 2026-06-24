from app.models.agent_run import AgentRun
from app.llm.registry import LLMRegistry
from app.llm.builder import PromptBuilder


class AgentRunner:
    @staticmethod
    def run(db, agent, version, input_text, model_name):

        result = AgentRunner.prompt_agent(agent, version, input_text, model_name)

        run = AgentRun(
            agent_id=agent.id,
            version_id=version.id,
            input_prompt=input_text,
            output=result["response"],
            model=model_name,
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
    def prompt_agent(agent, version, input_text, model_name):

        system_prompt, user_prompt = PromptBuilder.build(version, input_text)

        llm = LLMRegistry.get_provider(model_name)

        output = llm.generate(system_prompt, user_prompt)

        return {
            "agent_id": str(agent.id),
            "version": version.version,
            "prompt_used": version.prompt,
            "response": output,  # f"[MOCK RESPONSE] executed prompt: {version.prompt}",
        }

    @staticmethod
    def list_runs(
        db,
        agent_id,
        version_id=None,
        limit: int = 20,
        offset: int = 0,
    ):
        query = db.query(AgentRun).filter(AgentRun.agent_id == agent_id)

        if version_id:
            query = query.filter(AgentRun.version_id == version_id)

        return (
            query.order_by(AgentRun.created_at.desc()).offset(offset).limit(limit).all()
        )
