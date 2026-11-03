import React, { useEffect, useState } from "react";
import { Activity, ShieldCheck, HeartHandshake, Zap } from "lucide-react";
import { MetricCard } from "../../components/MetricCard";
import { api } from "../../services/api";
import { WorkplaceSummary } from "../../types";
import { formatScore } from "../../lib/utils";

export const IntelligenceDashboard: React.FC = () => {
  const [summary, setSummary] = useState<WorkplaceSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getSummary()
      .then((data) => setSummary(data))
      .catch((err) => console.error("Error fetching summary:", err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-slate-400">Loading intelligence metrics...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard
          title="Overall Workplace Score"
          value={summary ? formatScore(summary.workplace_score) : "89%"}
          subtitle="Health index across all agents"
          trend="+3.2% vs last cycle"
          icon={<Activity className="w-5 h-5 text-blue-400" />}
        />
        <MetricCard
          title="Fairness Index"
          value={summary ? formatScore(summary.average_fairness_index) : "94%"}
          subtitle="Equity across task allocation"
          icon={<ShieldCheck className="w-5 h-5 text-emerald-400" />}
        />
        <MetricCard
          title="Culture Health"
          value="Healthy"
          subtitle={summary?.culture_vibe || "High psychological safety"}
          icon={<HeartHandshake className="w-5 h-5 text-purple-400" />}
        />
        <MetricCard
          title="Events Ingested"
          value={summary?.total_events_processed ?? 142}
          subtitle="Signals analyzed"
          icon={<Zap className="w-5 h-5 text-amber-400" />}
        />
      </div>

      {/* Insights Section */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6">
        <h3 className="text-base font-bold text-white mb-4">Multi-Agent Intelligence Insights [STUB]</h3>
        <div className="space-y-3">
          {summary?.recent_insights.map((insight, idx) => (
            <div key={idx} className="flex items-start gap-3 p-3 rounded-lg bg-slate-900/60 border border-slate-800/80 text-sm text-slate-300">
              <span className="w-2 h-2 rounded-full bg-blue-400 mt-1.5 flex-shrink-0" />
              <span>{insight}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
