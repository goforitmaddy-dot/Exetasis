import React from "react";
import { AgentInspector } from "../features/agents/AgentInspector";

export const AgentsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Multi-Agent Intelligence Network</h2>
        <p className="text-xs text-slate-400">
          8 specialized LangGraph agents running open-weight local LLMs to assess workplace dynamics.
        </p>
      </div>

      <AgentInspector />
    </div>
  );
};
