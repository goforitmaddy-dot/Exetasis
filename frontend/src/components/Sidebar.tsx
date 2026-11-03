import React from "react";
import { LayoutDashboard, Box, Bot, UserCheck } from "lucide-react";
import { useAppStore, NavTab } from "../store/useAppStore";
import { cn } from "../lib/utils";

export const Sidebar: React.FC = () => {
  const { activeTab, setActiveTab } = useAppStore();

  const navItems: { id: NavTab; label: string; icon: React.ReactNode }[] = [
    { id: "dashboard", label: "Dashboard", icon: <LayoutDashboard className="w-5 h-5" /> },
    { id: "digital-twin", label: "3D Digital Twin", icon: <Box className="w-5 h-5" /> },
    { id: "agents", label: "Multi-Agent System", icon: <Bot className="w-5 h-5" /> },
    { id: "onboarding", label: "Workplace Setup", icon: <UserCheck className="w-5 h-5" /> },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-[#0B0F19] flex flex-col justify-between p-4">
      <nav className="flex flex-col gap-1.5">
        <div className="px-3 py-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
          Navigation
        </div>
        {navItems.map((item) => {
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors text-left",
                isActive
                  ? "bg-blue-600/10 text-blue-400 border border-blue-500/20"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
              )}
            >
              {item.icon}
              {item.label}
            </button>
          );
        })}
      </nav>

      <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-400">
        <p className="font-semibold text-slate-300">Hackathon Foundation</p>
        <p className="mt-1 text-[11px] text-slate-500">Local LLM + LangGraph Orchestration</p>
      </div>
    </aside>
  );
};
