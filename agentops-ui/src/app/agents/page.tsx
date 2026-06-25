"use client";

import { useEffect, useState } from "react";
import { createAgent, getAgents } from "@/lib/api";
import Link from "next/link";

export default function AgentsPage() {
  const [agents, setAgents] = useState([]);
  const [error, setError] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [owner, setOwner] = useState("");

  async function loadAgents() {
    getAgents()
      .then(setAgents)
      .catch((err) => {
        console.error(err);
        setError("Failed to load agents");
      });
  }

  useEffect(() => {
    loadAgents();
  }, []);

  async function handleCreateAgent() {
    if (!name.trim() || !owner.trim()) {
      return;
    }

    try {
      setError("");
      await createAgent({
        name,
        description,
        owner,
      });
      setName("");
      setDescription("");
      setOwner("");
      await loadAgents();
    } catch (err) {
      console.error(err);
      setError("Failed to create agent");
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Agents</h1>

      {error && (
        <div className="mb-4 text-red-600">
          {error}
        </div>
      )}

      <div className="mb-6 space-y-3 border rounded p-4">
        <h2 className="text-lg font-semibold">Create Agent</h2>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full border rounded p-2"
          placeholder="Agent name"
        />
        <input
          value={owner}
          onChange={(e) => setOwner(e.target.value)}
          className="w-full border rounded p-2"
          placeholder="Owner"
        />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border rounded p-2"
          rows={3}
          placeholder="Description"
        />
        <button
          type="button"
          onClick={handleCreateAgent}
          className="px-4 py-2 border rounded"
        >
          Create
        </button>
      </div>

      <div className="space-y-2">
        {agents.map((agent: any) => (
        <Link
            href={`/agents/${agent.id}`}
            key={agent.id}
        >
            <div className="border p-3 rounded hover:bg-gray-100 cursor-pointer">
            <div className="font-semibold">{agent.name}</div>
            <div className="text-sm text-gray-500">
                {agent.description}
            </div>
            </div>
        </Link>
        ))}
      </div>
    </div>
  );
}
