import React from "react";
import { OnboardingWizard } from "../features/onboarding/OnboardingWizard";

export const OnboardingPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h2 className="text-xl font-bold text-white">Workplace Setup & Onboarding</h2>
        <p className="text-xs text-slate-400">Initialize workspace configuration, layout topology, and adapter pipelines.</p>
      </div>

      <OnboardingWizard />
    </div>
  );
};
