import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Compass, ShieldCheck, Box } from "lucide-react";
import { MultilingualGreeting } from "../../components/common/MultilingualGreeting";
import { InteractiveHeroNodes } from "../../components/common/InteractiveHeroNodes";
import { useLanguageStore } from "../../store/useLanguageStore";

export const HeroSection: React.FC = () => {
  const { t } = useLanguageStore();

  const handleScrollToExplore = (e: React.MouseEvent) => {
    e.preventDefault();
    const target = document.getElementById("capabilities");
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section className="relative min-h-[calc(100vh-4rem)] flex items-center justify-center overflow-hidden px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
      {/* Background Interactive Nodes Canvas */}
      <InteractiveHeroNodes />

      {/* Radial Depth Lighting */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] sm:w-[900px] h-[500px] bg-gradient-to-tr from-blue-600/15 via-indigo-600/10 to-transparent rounded-full blur-[160px] pointer-events-none" />

      {/* Main Container */}
      <div className="relative z-10 max-w-5xl mx-auto text-center space-y-8">
        {/* Animated Multilingual Greeting Header Pill */}
        <div className="flex justify-center animate-in fade-in slide-in-from-bottom-3 duration-500">
          <MultilingualGreeting />
        </div>

        {/* Hero Title */}
        <div className="space-y-4">
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold text-white tracking-tight leading-[1.08] sm:leading-[1.05]">
            <span className="block font-sans">
              {t("hero.headline", "Workplaces that understand themselves.")}
            </span>
          </h1>

          <p className="max-w-3xl mx-auto text-base sm:text-lg lg:text-xl text-slate-300 font-normal leading-relaxed">
            {t(
              "hero.subheadline",
              "An intelligent workplace orchestration platform that transforms organizational events into meaningful insights through adaptive AI agents and a living digital twin."
            )}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Link
            to="/register"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-500 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-sm sm:text-base shadow-xl shadow-blue-600/30 hover:shadow-blue-600/50 hover:scale-[1.02] transition-all duration-200"
          >
            <span>{t("hero.getStarted", "Get Started")}</span>
            <ArrowRight className="w-4 h-4" />
          </Link>

          <a
            href="#capabilities"
            onClick={handleScrollToExplore}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-200 hover:text-white font-semibold text-sm sm:text-base border border-slate-700/80 hover:border-slate-600 backdrop-blur-md transition-all duration-200"
          >
            <Compass className="w-4 h-4 text-blue-400" />
            <span>{t("hero.explore", "Explore Exetasis")}</span>
          </a>
        </div>

        {/* Live System Indicator Pills */}
        <div className="pt-8 flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-xs text-slate-400 border-t border-slate-800/80 max-w-2xl mx-auto">
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/60 border border-slate-800">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>8 Autonomous Agents Online</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/60 border border-slate-800">
            <Box className="w-3.5 h-3.5 text-blue-400" />
            <span>3D Digital Twin Synchronized</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900/60 border border-slate-800">
            <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
            <span>Privacy-Preserving Telemetry</span>
          </div>
        </div>
      </div>
    </section>
  );
};
