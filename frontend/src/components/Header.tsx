import React from "react";
import { Activity, Radio } from "lucide-react";
import { useTwinStore } from "../store/useTwinStore";

export const Header: React.FC = () => {
  const { nodes } = useTwinStore();
  const activeCount = nodes.filter((n) => n.status === "active" || n.status === "collaborating").length;

  return (
    <header className="h-16 border-b border-slate-800 bg-[#0B0F19]/80 backdrop-blur-md px-6 flex items-center justify-between z-20">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-base font-bold text-white tracking-wide">Exetasis</h1>
          <p className="text-[11px] text-slate-400">Workplace Intelligence Platform</p>
        </div>
      </div>

      <div className="flex items-center gap-4 text-xs text-slate-300">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800">
          <Radio className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span>Live Twin Sync</span>
          <span className="text-slate-500">|</span>
          <span className="font-semibold text-emerald-400">{activeCount}</span>
          <span className="text-slate-400">Active</span>
        </div>
      </div>
    </header>
  );
};
