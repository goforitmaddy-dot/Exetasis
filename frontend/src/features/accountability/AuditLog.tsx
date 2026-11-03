import React from "react";
import { CheckSquare, ShieldCheck } from "lucide-react";

export const AuditLog: React.FC = () => {
  return (
    <div className="bg-[#111827] border border-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <ShieldCheck className="w-5 h-5 text-indigo-400" />
        <h4 className="text-sm font-bold text-white uppercase tracking-wider">Accountability Audit [STUB]</h4>
      </div>
      <p className="text-xs text-slate-400 mb-4">
        Blameless tracking of retro commitments, team SLAs, and action resolution logs.
      </p>

      <div className="space-y-2">
        <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-200">
            <CheckSquare className="w-4 h-4 text-emerald-400" />
            <span>Database failover drill verified</span>
          </div>
          <span className="text-[10px] text-slate-400">Resolved</span>
        </div>
      </div>
    </div>
  );
};
