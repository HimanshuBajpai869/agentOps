class PromptBuilder:

    @staticmethod
    def build(version, input_text: str):

        system_prompt = "You are a helpful AI agent."

        user_prompt = f"""
Agent Instruction:
{version.prompt}

---

User Input:
{input_text}
"""

        return system_prompt, user_prompt
