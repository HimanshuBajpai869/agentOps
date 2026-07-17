import requests


class AgentOpsClient:

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
    ):
        self.base_url = base_url.rstrip("/")

    def create_agent(
        self,
        name: str,
        description: str,
        owner: str,
    ):

        response = requests.post(
            f"{self.base_url}/agents",
            json={
                "name": name,
                "description": description,
                "owner": owner,
            },
        )

        response.raise_for_status()

        return response.json()

    def list_agents(self):

        response = requests.get(
            f"{self.base_url}/agents",
        )

        response.raise_for_status()

        return response.json()
