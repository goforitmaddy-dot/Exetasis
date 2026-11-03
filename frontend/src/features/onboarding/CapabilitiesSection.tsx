import React from "react";
import { Cpu, Scale, HeartPulse, Award, Box, ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";
import { useLanguageStore } from "../../store/useLanguageStore";

export const CapabilitiesSection: React.FC = () => {
  const { t } = useLanguageStore();

  const capabilities = [
    {
      id: "adaptive-intelligence",
      title: t("capabilities.cap1_title", "Adaptive Workplace Intelligence"),
      desc: t(
        "capabilities.cap1_desc",
        "Autonomous LangGraph agents model workplace dynamics across physical floorplans and remote communication streams."
      ),
      icon: <Cpu className="w-5 h-5 text-blue-400" />,
      accent: "from-blue-500/20 to-transparent",
      border: "hover:border-blue-500/40",
      badge: "Architect & Configuration",
    },
    {
      id: "contribution-fairness",
      title: t("capabilities.cap2_title", "Contribution & Fairness Analysis"),
      desc: t(
        "capabilities.cap2_desc",
        "Continuous evaluation of meaningful impact, peer support, and equitable task distribution without vanity metrics."
      ),
      icon: <Scale className="w-5 h-5 text-emerald-400" />,
      accent: "from-emerald-500/20 to-transparent",
      border: "hover:border-emerald-500/40",
      badge: "Equity & Impact",
    },
    {
      id: "culture-environment",
      title: t("capabilities.cap3_title", "Workplace Culture & Environment"),
      desc: t(
        "capabilities.cap3_desc",
        "Real-time telemetry measuring team camaraderie, psychological safety, and ambient acoustic comfort."
      ),
      icon: <HeartPulse className="w-5 h-5 text-purple-400" />,
      accent: "from-purple-500/20 to-transparent",
      border: "hover:border-purple-500/40",
      badge: "Sensory & Vibe",
    },
    {
      id: "accountability-rewards",
      title: t("capabilities.cap4_title", "AI-Powered Accountability & Rewards"),
      desc: t(
        "capabilities.cap4_desc",
        "Blameless SLA tracking, commitment fulfillment, and automated equitable kudos token rewards."
      ),
      icon: <Award className="w-5 h-5 text-amber-400" />,
      accent: "from-amber-500/20 to-transparent",
      border: "hover:border-amber-500/40",
      badge: "Blameless SLAs",
    },
    {
      id: "digital-twin",
      title: t("capabilities.cap5_title", "Real-Time 3D Digital Twin"),
      desc: t(
        "capabilities.cap5_desc",
        "Spatial WebGL digital twin rendering employee nodes, collaboration zones, and telemetry pulses in real time."
      ),
      icon: <Box className="w-5 h-5 text-indigo-400" />,
      accent: "from-indigo-500/20 to-transparent",
      border: "hover:border-indigo-500/40",
      badge: "Three.js & WebGL",
      span2: true,
    },
  ];

  return (
    <section id="capabilities" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto scroll-mt-20">
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-xs font-semibold uppercase tracking-wider text-blue-400">
          {t("capabilities.badge", "Core Architecture")}
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          {t("capabilities.title", "Autonomous Multi-Agent Workplace Intelligence")}
        </h2>
        <p className="text-slate-400 text-sm sm:text-base">
          {t(
            "capabilities.subtitle",
            "Five interconnected pillars delivering transparency, psychological safety, and organizational clarity."
          )}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {capabilities.map((cap) => (
          <div
            key={cap.id}
            className={`group relative bg-[#101827]/90 border border-slate-800 rounded-2xl p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-blue-900/10 flex flex-col justify-between ${
              cap.border
            } ${cap.span2 ? "md:col-span-2 lg:col-span-2 bg-gradient-to-br from-indigo-950/20 via-[#101827] to-[#101827]" : ""}`}
          >
            <div>
              <div className="flex items-center justify-between mb-4">
                <div className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center shadow-inner">
                  {cap.icon}
                </div>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-slate-900/80 border border-slate-700/60 text-slate-300">
                  {cap.badge}
                </span>
              </div>
              <h3 className="text-base sm:text-lg font-bold text-white mb-2 group-hover:text-blue-300 transition-colors">
                {cap.title}
              </h3>
              <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">{cap.desc}</p>
            </div>

            <div className="pt-6 mt-4 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-500">
              <span className="font-mono text-[11px]">LangGraph Multi-Agent Node</span>
              <Link
                to="/register"
                className="text-blue-400 hover:text-blue-300 flex items-center gap-1 font-semibold group-hover:translate-x-0.5 transition-transform"
              >
                <span>Launch</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
