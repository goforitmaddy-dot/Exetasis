import React from "react";
import { CheckCircle2, Sliders } from "lucide-react";

export const OnboardingWizard: React.FC = () => {
  return (
    <div className="bg-[#111827] border border-slate-800 rounded-xl p-6">
      <div className="flex items-center gap-3 mb-4">
        <Sliders className="w-5 h-5 text-blue-400" />
        <h2 className="text-lg font-bold text-white">Workplace Architecture Setup [STUB]</h2>
      </div>
      <p className="text-sm text-slate-400 mb-6">
        Configure initial organizational layout parameters, department boundaries, and event adapter webhooks.
      </p>

      <div className="space-y-4">
        <div className="flex items-center justify-between p-3.5 rounded-lg bg-slate-900 border border-slate-800">
          <div>
            <div className="text-sm font-semibold text-white">Slack Communication Ingestion</div>
            <div className="text-xs text-slate-400">Adapter: SlackAdapter [STUB]</div>
          </div>
          <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Ready
          </span>
        </div>

        <div className="flex items-center justify-between p-3.5 rounded-lg bg-slate-900 border border-slate-800">
          <div>
            <div className="text-sm font-semibold text-white">GitHub Repository Signals</div>
            <div className="text-xs text-slate-400">Adapter: GitHubAdapter [STUB]</div>
          </div>
          <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Ready
          </span>
        </div>

        <div className="flex items-center justify-between p-3.5 rounded-lg bg-slate-900 border border-slate-800">
          <div>
            <div className="text-sm font-semibold text-white">Calendar & Meeting Sync</div>
            <div className="text-xs text-slate-400">Adapter: CalendarAdapter [STUB]</div>
          </div>
          <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Ready
          </span>
        </div>
      </div>
    </div>
  );
};
