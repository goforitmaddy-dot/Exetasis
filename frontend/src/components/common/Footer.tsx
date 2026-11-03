import React from "react";
import { BrandLogo } from "./BrandLogo";
import { useLanguageStore } from "../../store/useLanguageStore";

export const Footer: React.FC = () => {
  const { t } = useLanguageStore();

  return (
    <footer className="border-t border-slate-800/80 bg-[#070B16] text-slate-400 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex flex-col items-center md:items-start gap-2">
          <BrandLogo size="sm" />
          <p className="text-xs text-slate-500 max-w-sm text-center md:text-left mt-1">
            {t("footer.tagline", "Living Digital Twin & Multi-Agent Workplace Intelligence.")}
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-6 text-xs text-slate-400">
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[11px] text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>{t("footer.systemStatus", "All Systems Operational")}</span>
          </div>
          <span>&copy; {new Date().getFullYear()} Exetasis Platform.</span>
        </div>
      </div>
    </footer>
  );
};
