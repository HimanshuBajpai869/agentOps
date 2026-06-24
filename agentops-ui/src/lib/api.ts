const BASE_URL = "http://localhost:8000";

export async function getAgents() {
  const res = await fetch(`${BASE_URL}/agents`);
  return res.json();
}

export async function getAgent(id: string) {
  const res = await fetch(`${BASE_URL}/agents/${id}`);
  return res.json();
}

export async function getRuns(agentId: string) {
  const res = await fetch(
    `${BASE_URL}/agents/${agentId}/runs?limit=20&offset=0`
  );

  return res.json();
}

export async function runAgent(
  agentId: string,
  inputPrompt: string
) {
  const params = new URLSearchParams({
    input_text: inputPrompt,
    model_name: "tinyllama",
  });

  const res = await fetch(
    `${BASE_URL}/agents/${agentId}/run?${params.toString()}`,
    {
      method: "POST",
    }
  );

  return res.json();
}