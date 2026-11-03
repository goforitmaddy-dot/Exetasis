import React from "react";
import { IntelligenceDashboard } from "../features/dashboard/IntelligenceDashboard";
import { RewardCenter } from "../features/rewards/RewardCenter";
import { AuditLog } from "../features/accountability/AuditLog";

export const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white">Workplace Intelligence Overview</h2>
        <p className="text-xs text-slate-400">Continuous telemetry and multi-agent organizational evaluation.</p>
      </div>

      <IntelligenceDashboard />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RewardCenter />
        <AuditLog />
      </div>
    </div>
  );
};
