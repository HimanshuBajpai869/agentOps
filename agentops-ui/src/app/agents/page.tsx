"use client";

import { useEffect, useState } from "react";
import { getAgents } from "@/lib/api";
import Link from "next/link";

export default function AgentsPage() {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    getAgents().then(setAgents);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Agents</h1>

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