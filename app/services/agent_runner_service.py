from app.llm.registry import LLMRegistry
from app.llm.builder import PromptBuilder
from app.repositories.sqlalchemy.run_repository import SQLAlchemyRunRepository
from app.services.tracer_service import TracerService


class AgentRunner:
    @staticmethod
    def run(tracer: TracerService, agent, version, input_text, model_name):
        run = tracer.start_run(
            agent_id=agent.id,
            version_id=version.id,
            input_prompt=input_text,
            model=model_name,
            metadata={
                "agent_name": agent.name,
                "agent_version": version.version,
            },
        )

        try:
            result = AgentRunner.prompt_agent(
                tracer=tracer,
                run_id=run.id,
                agent=agent,
                version=version,
                input_text=input_text,
                model_name=model_name,
            )
            run = tracer.complete_run(run.id, output=result["response"])
        except Exception as error:
            tracer.fail_run(run.id, error)
            raise

        return {
            "run_id": run.id,
            "agent_id": agent.id,
            "version_id": version.id,
            "response": result["response"],
            "output": result["response"],
        }

    @staticmethod
    def prompt_agent(tracer: TracerService, run_id, agent, version, input_text, model_name):
        system_prompt, user_prompt = PromptBuilder.build(version, input_text)
        llm = LLMRegistry.get_provider(model_name)
        output = tracer.trace_llm_call(
            run_id=run_id,
            name="llm.generate",
            metadata={
                "model": model_name,
                "provider": llm.__class__.__name__,
            },
            operation=lambda: llm.generate(system_prompt, user_prompt),
        )

        return {
            "agent_id": str(agent.id),
            "version": version.version,
            "prompt_used": version.prompt,
            "response": output,
        }

    @staticmethod
    def list_runs(
        db,
        agent_id,
        version_id=None,
        limit: int = 20,
        offset: int = 0,
    ):
        return SQLAlchemyRunRepository(db).list_by_agent(
            agent_id=agent_id,
            version_id=version_id,
            limit=limit,
            offset=offset,
        )
