import React from "react";
import { Link } from "react-router-dom";
import { BrandLogo } from "../common/BrandLogo";
import { LanguageSelector } from "../common/LanguageSelector";
import { Sparkles, Shield, Cpu, Box } from "lucide-react";
import { useLanguageStore } from "../../store/useLanguageStore";

interface Props {
  children: React.ReactNode;
  title: string;
  subtitle: string;
}

export const AuthLayout: React.FC<Props> = ({ children, title, subtitle }) => {
  const { t } = useLanguageStore();

  return (
    <div className="min-h-screen w-full bg-[#0B1020] text-slate-100 flex flex-col justify-between relative overflow-hidden">
      {/* Background Ambient Glows */}
      <div className="absolute top-0 left-1/4 w-[600px] h-[400px] bg-blue-600/10 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-[500px] h-[400px] bg-violet-600/10 rounded-full blur-[140px] pointer-events-none" />

      {/* Header Bar */}
      <header className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between z-10">
        <BrandLogo size="md" />
        <div className="flex items-center gap-4">
          <LanguageSelector compact={false} />
          <Link
            to="/"
            className="text-xs font-semibold text-slate-400 hover:text-white transition-colors"
          >
            ← {t("nav.explore", "Back to Home")}
          </Link>
        </div>
      </header>

      {/* Main Content Split / Centered Grid */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-8 z-10">
        <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          {/* Left / Top Form Card */}
          <div className="lg:col-span-7 bg-[#101827]/90 border border-slate-800/90 rounded-2xl p-6 sm:p-10 shadow-2xl shadow-black/60 backdrop-blur-xl">
            <div className="mb-6">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                {title}
              </h1>
              <p className="mt-2 text-sm text-slate-400">{subtitle}</p>
            </div>
            {children}
          </div>

          {/* Right Brand Showcase Panel (Visible on Desktop/Laptop) */}
          <div className="hidden lg:flex lg:col-span-5 flex-col justify-between space-y-6">
            <div className="bg-gradient-to-br from-slate-900/80 to-[#101827]/80 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-md shadow-xl">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400 mb-3">
                <Sparkles className="w-4 h-4" />
                <span>Next-Gen Workplace Intelligence</span>
              </div>
              <h3 className="text-lg font-bold text-white leading-snug">
                Autonomous multi-agent orchestration for human-centered organizations.
              </h3>
              <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                Seamlessly synthesize collaboration signals, detect toil imbalances, and observe
                real-time spatial interactions in our living 3D digital twin.
              </p>

              <div className="mt-6 space-y-3 pt-6 border-t border-slate-800">
                <div className="flex items-center gap-3 text-xs text-slate-300">
                  <div className="w-7 h-7 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-400 flex-shrink-0">
                    <Box className="w-3.5 h-3.5" />
                  </div>
                  <span>Real-time spatial digital twin with WebGL telemetry</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-300">
                  <div className="w-7 h-7 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-400 flex-shrink-0">
                    <Cpu className="w-3.5 h-3.5" />
                  </div>
                  <span>8 specialized LangGraph agents running open-weight local models</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-300">
                  <div className="w-7 h-7 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400 flex-shrink-0">
                    <Shield className="w-3.5 h-3.5" />
                  </div>
                  <span>Blameless accountability, equity auditing & privacy-first design</span>
                </div>
              </div>
            </div>

            <div className="px-4 py-3 rounded-xl bg-slate-900/50 border border-slate-800/60 text-[11px] text-slate-400 flex items-center justify-between">
              <span>Trusted across high-compliance industries</span>
              <span className="text-emerald-400 font-medium">Enterprise Ready</span>
            </div>
          </div>
        </div>
      </main>

      {/* Subtle Footer note */}
      <footer className="w-full text-center py-4 text-xs text-slate-500 z-10">
        &copy; {new Date().getFullYear()} Exetasis Platform. Built for intelligent workplaces.
      </footer>
    </div>
  );
};
