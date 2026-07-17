const BASE_URL = "/api";

export type RunRecord = {
  id: string;
  agent_id: string;
  version_id: string;
  input_prompt: string | null;
  output: string | null;
  created_at: string;
  started_at: string;
  ended_at: string | null;
  duration_ms: number | null;
  status: string;
  error_type: string | null;
  error_message: string | null;
  model: string;
  metadata: Record<string, unknown>;
};

export type SpanRecord = {
  id: string;
  run_id: string;
  parent_span_id: string | null;
  name: string;
  span_type: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  duration_ms: number | null;
  error_type: string | null;
  error_message: string | null;
  metadata: Record<string, unknown>;
};

export type TimelineRecord = {
  run: RunRecord;
  spans: SpanRecord[];
};

export async function createAgent(payload: {
  name: string;
  description?: string;
  owner: string;
}) {
  const res = await fetch(`${BASE_URL}/agents`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`Failed to create agent: ${res.status}`);
  }

  return res.json();
}

export async function getAgents() {
  const res = await fetch(`${BASE_URL}/agents`);

  if (!res.ok) {
    throw new Error(`Failed to load agents: ${res.status}`);
  }

  return res.json();
}

export async function getAgent(id: string) {
  const res = await fetch(`${BASE_URL}/agents/${id}`);

  if (!res.ok) {
    throw new Error(`Failed to load agent: ${res.status}`);
  }

  return res.json();
}

export async function getRuns(agentId: string) {
  const res = await fetch(
    `${BASE_URL}/agents/${agentId}/runs?limit=20&offset=0`
  );

  if (!res.ok) {
    throw new Error(`Failed to load runs: ${res.status}`);
  }

  return res.json() as Promise<RunRecord[]>;
}

export async function getTimeline(
  agentId: string,
  runId: string
) {
  const res = await fetch(
    `${BASE_URL}/agents/${agentId}/runs/${runId}/timeline`
  );

  if (!res.ok) {
    throw new Error(`Failed to load timeline: ${res.status}`);
  }

  return res.json() as Promise<TimelineRecord>;
}

export async function createVersion(
  agentId: string,
  payload: {
    version: string;
    prompt?: string;
    agent_config?: string;
  }
) {
  const res = await fetch(`${BASE_URL}/agents/${agentId}/versions`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`Failed to create version: ${res.status}`);
  }

  return res.json();
}

export async function activateVersion(agentId: string, versionId: string) {
  const res = await fetch(
    `${BASE_URL}/agents/${agentId}/activate/${versionId}`,
    {
      method: "POST",
    }
  );

  if (!res.ok) {
    throw new Error(`Failed to activate version: ${res.status}`);
  }

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

  if (!res.ok) {
    throw new Error(`Failed to run agent: ${res.status}`);
  }

  return res.json();
}

export async function getAgentVersion(
  agentId: string,
  agentVersionId: string
) {
  const res = await fetch(`${BASE_URL}/agents/${agentId}/versions/${agentVersionId}`);

  if (!res.ok) {
    throw new Error(`Failed to get version details: ${res.status}`);
  }

  return res.json();
}