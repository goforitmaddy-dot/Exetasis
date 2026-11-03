import { create } from "zustand";
import { WorkplaceSummary } from "../types";

export type NavTab = "dashboard" | "digital-twin" | "agents" | "onboarding";

interface AppStoreState {
  activeTab: NavTab;
  summary: WorkplaceSummary | null;
  setActiveTab: (tab: NavTab) => void;
  setSummary: (summary: WorkplaceSummary) => void;
}

export const useAppStore = create<AppStoreState>((set) => ({
  activeTab: "dashboard",
  summary: null,
  setActiveTab: (tab) => set({ activeTab: tab }),
  setSummary: (summary) => set({ summary }),
}));
