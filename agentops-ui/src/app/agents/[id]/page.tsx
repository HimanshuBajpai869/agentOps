"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  activateVersion,
  createVersion,
  getAgent,
  getRuns,
  getTimeline,
  runAgent,
  type RunRecord,
  type TimelineRecord,
} from "@/lib/api";

export default function AgentDetail() {
  const params = useParams();
  const agentId = params.id as string;
  const [agent, setAgent] = useState<any>(null);
  const [runs, setRuns] = useState<RunRecord[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [timeline, setTimeline] = useState<TimelineRecord | null>(null);
  const [timelineLoading, setTimelineLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [running, setRunning] = useState(false);
  const [versionName, setVersionName] = useState("");
  const [versionPrompt, setVersionPrompt] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const agentData = await getAgent(agentId);
        const runsData = await getRuns(agentId);

        setAgent(agentData);
        setRuns(runsData);
        setSelectedRunId(runsData[0]?.id ?? null);
      } catch (err) {
        console.error(err);
        setError("Failed to load agent");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [params.id]);

  useEffect(() => {
    async function loadTimeline() {
      if (!selectedRunId) {
        setTimeline(null);
        return;
      }

      setTimelineLoading(true);

      try {
        const timelineData = await getTimeline(agentId, selectedRunId);
        setTimeline(timelineData);
      } catch (err) {
        console.error(err);
        setTimeline(null);
      } finally {
        setTimelineLoading(false);
      }
    }

    loadTimeline();
  }, [agentId, selectedRunId]);

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
      setSelectedRunId(result.run_id);

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

      <div className="border rounded p-4 space-y-3">
        <h2 className="text-xl font-semibold">Version</h2>
        <input
          value={versionName}
          onChange={(e) => setVersionName(e.target.value)}
          className="w-full border rounded p-2"
          placeholder="Version name"
        />
        <textarea
          value={versionPrompt}
          onChange={(e) => setVersionPrompt(e.target.value)}
          className="w-full border rounded p-2"
          rows={4}
          placeholder="Version prompt"
        />
        <div className="flex gap-3">
          <button
            type="button"
            onClick={async () => {
              if (!versionName.trim()) {
                return;
              }

              try {
                const version = await createVersion(agentId, {
                  version: versionName,
                  prompt: versionPrompt,
                  agent_config: "{}",
                });
                const updatedAgent = await activateVersion(agentId, version.id);
                setAgent(updatedAgent);
                setVersionName("");
                setVersionPrompt("");
              } catch (err) {
                console.error(err);
                setError("Failed to create version");
              }
            }}
            className="px-4 py-2 border rounded"
          >
            Create and Activate
          </button>
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
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(320px,420px)]">
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
              <button
                key={run.id}
                type="button"
                onClick={() => setSelectedRunId(run.id)}
                className={`block w-full border rounded p-4 text-left ${
                  selectedRunId === run.id ? "bg-gray-50 border-black" : ""
                }`}
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

                <div>
                  <span className="font-semibold">
                    Status:
                  </span>{" "}
                  {run.status}
                </div>

                <div>
                  <span className="font-semibold">
                    Duration:
                  </span>{" "}
                  {run.duration_ms ?? "N/A"} ms
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

                {run.error_message && (
                  <div className="mt-2 text-sm text-red-600">
                    {run.error_type}: {run.error_message}
                  </div>
                )}
              </button>
            ))}
          </div>
        )}
        </div>

        <div className="border rounded p-4 h-fit">
          <h2 className="text-xl font-semibold mb-4">
            Timeline
          </h2>

          {!selectedRunId ? (
            <div className="text-gray-500">
              Select a run to inspect.
            </div>
          ) : timelineLoading ? (
            <div className="text-gray-500">
              Loading timeline...
            </div>
          ) : !timeline ? (
            <div className="text-gray-500">
              Timeline unavailable.
            </div>
          ) : timeline.spans.length === 0 ? (
            <div className="text-gray-500">
              No spans captured for this run.
            </div>
          ) : (
            <div className="space-y-3">
              {timeline.spans.map((span) => (
                <div
                  key={span.id}
                  className="border rounded p-3"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="font-semibold">
                      {span.name}
                    </div>

                    <div className="text-xs uppercase text-gray-500">
                      {span.span_type}
                    </div>
                  </div>

                  <div className="mt-2 text-sm text-gray-600">
                    {span.status} • {span.duration_ms ?? "N/A"} ms
                  </div>

                  {span.error_message && (
                    <div className="mt-2 text-sm text-red-600">
                      {span.error_type}: {span.error_message}
                    </div>
                  )}

                  {Object.keys(span.metadata || {}).length > 0 && (
                    <pre className="mt-2 overflow-x-auto rounded bg-gray-50 p-2 text-xs whitespace-pre-wrap">
                      {JSON.stringify(span.metadata, null, 2)}
                    </pre>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

    </div>
  );
}
