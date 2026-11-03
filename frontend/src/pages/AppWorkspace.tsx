import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { Header } from "../components/Header";
import { Sidebar } from "../components/Sidebar";
import { useAppStore } from "../store/useAppStore";
import { DashboardPage } from "./DashboardPage";
import { DigitalTwinPage } from "./DigitalTwinPage";
import { AgentsPage } from "./AgentsPage";
import { OnboardingPage } from "./OnboardingPage";
import { useDigitalTwin } from "../hooks/useDigitalTwin";

export const AppWorkspace: React.FC = () => {
  // Initialize digital twin snapshot and WebSocket listener
  useDigitalTwin();

  const { activeTab } = useAppStore();

  return (
    <div className="flex flex-col h-screen bg-[#090D16] text-slate-100 overflow-hidden">
      {/* Top Banner allowing return to Welcome Page */}
      <div className="bg-slate-900 border-b border-slate-800 px-4 py-1.5 flex items-center justify-between text-xs text-slate-400">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-blue-400 hover:text-blue-300 font-medium transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Exit to Welcome Page</span>
        </Link>
        <span className="hidden sm:inline-block text-[11px] text-slate-500">
          Live Digital Twin Workspace • LangGraph Multi-Agent Pipeline Connected
        </span>
      </div>

      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-6 bg-[#090D16]">
          {activeTab === "dashboard" && <DashboardPage />}
          {activeTab === "digital-twin" && <DigitalTwinPage />}
          {activeTab === "agents" && <AgentsPage />}
          {activeTab === "onboarding" && <OnboardingPage />}
        </main>
      </div>
    </div>
  );
};

export default AppWorkspace;
