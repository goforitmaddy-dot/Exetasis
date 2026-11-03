import React from "react";
import { Award, Gift } from "lucide-react";

export const RewardCenter: React.FC = () => {
  return (
    <div className="bg-[#111827] border border-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <Award className="w-5 h-5 text-amber-400" />
        <h4 className="text-sm font-bold text-white uppercase tracking-wider">Recognition & Rewards [STUB]</h4>
      </div>
      <p className="text-xs text-slate-400 mb-4">
        AI-recommended kudos and milestone token grants formulated by the Reward Agent.
      </p>

      <div className="p-3.5 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-amber-500/10 flex items-center justify-center text-amber-400">
            <Gift className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white">Migration Hero Kudos [STUB]</div>
            <div className="text-[11px] text-slate-400">+150 recognition tokens issued</div>
          </div>
        </div>
        <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20">
          Awarded
        </span>
      </div>
    </div>
  );
};
