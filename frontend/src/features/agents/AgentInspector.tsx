import React, { useEffect, useState } from "react";
import { Bot, Play } from "lucide-react";
import { api } from "../../services/api";
import { AgentMetadata } from "../../types";

export const AgentInspector: React.FC = () => {
  const [agents, setAgents] = useState<AgentMetadata[]>([]);
  const [evaluating, setEvaluating] = useState<string | null>(null);
  const [lastResult, setLastResult] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    api.getAgents().then(setAgents).catch(console.error);
  }, []);

  const handleTestAgent = async (agentId: string) => {
    setEvaluating(agentId);
    try {
      const res = await api.evaluateAgent(agentId, "target-team-lead");
      setLastResult(res as unknown as Record<string, unknown>);
    } catch (err) {
      console.error(err);
    } finally {
      setEvaluating(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {agents.map((agent) => (
          <div
            key={agent.agent_id}
            className="bg-[#111827] border border-slate-800 rounded-xl p-5 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="w-8 h-8 rounded bg-blue-500/10 flex items-center justify-center text-blue-400">
                  <Bot className="w-4 h-4" />
                </div>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  Active
                </span>
              </div>
              <h4 className="font-bold text-white text-sm">{agent.name}</h4>
              <p className="text-xs text-slate-400 mt-1 line-clamp-2">{agent.description}</p>
            </div>

            <button
              onClick={() => handleTestAgent(agent.agent_id)}
              disabled={evaluating === agent.agent_id}
              className="mt-4 w-full py-1.5 px-3 rounded-lg bg-blue-600/10 hover:bg-blue-600/20 text-blue-400 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors border border-blue-500/20 disabled:opacity-50"
            >
              <Play className="w-3 h-3" />
              {evaluating === agent.agent_id ? "Evaluating..." : "Run Stub Test"}
            </button>
          </div>
        ))}
      </div>

      {lastResult && (
        <div className="bg-[#111827] border border-slate-800 rounded-xl p-5">
          <h4 className="text-sm font-bold text-white mb-2">Latest Agent Evaluation Output [STUB]:</h4>
          <pre className="text-xs bg-slate-950 p-4 rounded-lg overflow-x-auto text-emerald-400 font-mono">
            {JSON.stringify(lastResult, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};
