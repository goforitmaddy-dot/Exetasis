import React from "react";
import { Navbar } from "../components/common/Navbar";
import { Footer } from "../components/common/Footer";
import { HeroSection } from "../features/onboarding/HeroSection";
import { CapabilitiesSection } from "../features/onboarding/CapabilitiesSection";
import { IndustryAdaptationSection } from "../features/onboarding/IndustryAdaptationSection";

export const WelcomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#0B1020] text-slate-100 flex flex-col selection:bg-blue-500/30 selection:text-white">
      <Navbar />
      <main className="flex-1">
        <HeroSection />
        <CapabilitiesSection />
        <IndustryAdaptationSection />
      </main>
      <Footer />
    </div>
  );
};

export default WelcomePage;
