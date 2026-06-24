"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  getAgent,
  getRuns,
  runAgent,
} from "@/lib/api";

export default function AgentDetail() {
  const params = useParams();
  const agentId = params.id as string;
  const [agent, setAgent] = useState<any>(null);
  const [runs, setRuns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [running, setRunning] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const agentData = await getAgent(agentId);
        const runsData = await getRuns(agentId);

        setAgent(agentData);
        setRuns(runsData);
      } catch (err) {
        console.error(err);
        setError("Failed to load agent");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [params.id]);

  async function handleRun() {
  if (!prompt.trim()) {
    return;
  }

  setRunning(true);

  try {
    const result = await runAgent(
      agentId,
      prompt,
    );

    setResponse(result.output);

    const updatedRuns = await getRuns(agentId);
    setRuns(updatedRuns);

  } catch (err) {
    console.error(err);
  } finally {
    setRunning(false);
  }
}
  if (loading) {
    return (
      <div className="p-6">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-600">
        {error}
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">

      {/* Header */}
      <div className="border rounded p-4">
        <h1 className="text-3xl font-bold">
          {agent.name}
        </h1>

        <p className="text-gray-600 mt-2">
          {agent.description}
        </p>

        <div className="mt-4 space-y-1 text-sm">
          <div>
            <span className="font-semibold">Owner:</span>{" "}
            {agent.owner}
          </div>

          <div>
            <span className="font-semibold">Active Version:</span>{" "}
            {agent.active_version_id ?? "Not Activated"}
          </div>
        </div>
      </div>

      {/* Run Agent */}
      <div className="border rounded p-4">
        <h2 className="text-xl font-semibold mb-4">
          Run Agent
        </h2>

        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="w-full border rounded p-2"
          rows={5}
          placeholder="Enter prompt..."
        />

        <button
          onClick={handleRun}
          disabled={running}
          className="mt-3 px-4 py-2 border rounded"
        >
          {running ? "Running..." : "Run"}
        </button>

        {response && (
          <div className="mt-4">
            <h3 className="font-semibold">
              Response
            </h3>

            <div className="border rounded p-3 mt-2 whitespace-pre-wrap">
              {response}
            </div>
          </div>
        )}
      </div>

      {/* Runs */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Run History
        </h2>

        {runs.length === 0 ? (
          <div className="text-gray-500">
            No runs found.
          </div>
        ) : (
          <div className="space-y-3">
            {runs.map((run) => (
              <div
                key={run.id}
                className="border rounded p-4"
              >
                <div className="text-xs text-gray-500 mb-2">
                  {run.created_at}
                </div>

                <div>
                  <span className="font-semibold">
                    Version:
                  </span>{" "}
                  {run.version_id}
                </div>

                <div>
                  <span className="font-semibold">
                    Model:
                  </span>{" "}
                  {run.model || "N/A"}
                </div>

                <div className="mt-2">
                  <div className="font-semibold">
                    Input
                  </div>

                  <div className="bg-gray-50 p-2 rounded">
                    {run.input_prompt}
                  </div>
                </div>

                <div className="mt-2">
                  <div className="font-semibold">
                    Output
                  </div>

                  <div className="bg-gray-50 p-2 rounded whitespace-pre-wrap">
                    {run.output}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}