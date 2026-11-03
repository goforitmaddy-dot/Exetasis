import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { ArrowRight, Menu, X } from "lucide-react";
import { BrandLogo } from "./BrandLogo";
import { LanguageSelector } from "./LanguageSelector";
import { useLanguageStore } from "../../store/useLanguageStore";

export const Navbar: React.FC = () => {
  const { t } = useLanguageStore();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isAuthPage = location.pathname === "/login" || location.pathname === "/register";

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-[#0B1020]/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <BrandLogo size="md" />

        {/* Center Nav Links (Hidden on mobile and Auth pages) */}
        {!isAuthPage && (
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
            <a
              href="#capabilities"
              className="hover:text-white transition-colors py-1"
            >
              {t("nav.capabilities", "Capabilities")}
            </a>
            <a
              href="#industries"
              className="hover:text-white transition-colors py-1"
            >
              {t("nav.industries", "Industries")}
            </a>
            <Link
              to="/app"
              className="text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1.5 py-1"
            >
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Digital Twin Workspace</span>
            </Link>
          </nav>
        )}

        {/* Right Actions */}
        <div className="flex items-center gap-3 sm:gap-4">
          {/* Interface Language Selector */}
          <LanguageSelector compact={false} />

          {location.pathname !== "/login" && (
            <Link
              to="/login"
              className="text-xs sm:text-sm font-medium text-slate-300 hover:text-white px-2.5 py-1.5 rounded-lg hover:bg-slate-800/60 transition-colors"
            >
              {t("nav.signIn", "Sign In")}
            </Link>
          )}

          {location.pathname !== "/register" && (
            <Link
              to="/register"
              className="hidden sm:inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 via-indigo-600 to-blue-500 hover:from-blue-500 hover:to-indigo-500 text-white text-xs sm:text-sm font-semibold shadow-lg shadow-blue-600/20 hover:shadow-blue-600/40 transition-all duration-200"
            >
              <span>{t("nav.getStarted", "Get Started")}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          )}

          {/* Mobile hamburger menu toggle (for landing page) */}
          {!isAuthPage && (
            <button
              type="button"
              onClick={() => setMobileMenuOpen((prev) => !prev)}
              aria-label="Toggle mobile menu"
              className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          )}
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {!isAuthPage && mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-800 bg-[#0B1020]/95 px-4 py-4 space-y-3 backdrop-blur-2xl animate-in slide-in-from-top-2 duration-200">
          <a
            href="#capabilities"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/80 hover:text-white"
          >
            {t("nav.capabilities", "Capabilities")}
          </a>
          <a
            href="#industries"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-800/80 hover:text-white"
          >
            {t("nav.industries", "Industries")}
          </a>
          <Link
            to="/app"
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-blue-400 hover:bg-slate-800/80"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Digital Twin Workspace</span>
          </Link>
          <div className="pt-2 border-t border-slate-800">
            <Link
              to="/register"
              onClick={() => setMobileMenuOpen(false)}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg bg-blue-600 text-white text-sm font-semibold"
            >
              <span>{t("nav.getStarted", "Get Started")}</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}
    </header>
  );
};
