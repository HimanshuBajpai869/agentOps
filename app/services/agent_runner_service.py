class AgentRunner:

    @staticmethod
    def run(agent, version):
        return {
            "agent_id": str(agent.id),
            "version": version.version,
            "prompt_used": version.prompt,
            "response": f"[MOCK RESPONSE] executed prompt: {version.prompt}",
        }
