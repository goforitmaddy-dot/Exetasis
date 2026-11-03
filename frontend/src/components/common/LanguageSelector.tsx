import React, { useEffect, useRef, useState } from "react";
import { Globe, Check, ChevronDown } from "lucide-react";
import {
  LANGUAGE_OPTIONS,
  SupportedLanguage,
  useLanguageStore,
} from "../../store/useLanguageStore";
import { cn } from "../../lib/utils";

interface Props {
  className?: string;
  compact?: boolean;
}

export const LanguageSelector: React.FC<Props> = ({ className, compact = false }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { currentLanguage, setLanguage } = useLanguageStore();

  const currentOption =
    LANGUAGE_OPTIONS.find((opt) => opt.code === currentLanguage) || LANGUAGE_OPTIONS[0];

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={dropdownRef} className={cn("relative inline-block text-left", className)}>
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        className={cn(
          "flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-700/80 bg-slate-900/80 hover:bg-slate-800 text-slate-200 text-xs font-medium backdrop-blur-sm transition-all focus:outline-none focus:ring-2 focus:ring-blue-500/50",
          isOpen && "ring-2 ring-blue-500/40 border-blue-500/50"
        )}
      >
        <Globe className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" />
        <span className="flex items-center gap-1.5">
          <span>{currentOption.flag}</span>
          {!compact && (
            <span className="hidden sm:inline-block">
              {currentOption.name}
              <span className="text-slate-400 text-[10px] ml-1">({currentOption.nativeName})</span>
            </span>
          )}
          {compact && <span className="uppercase text-[11px] font-bold">{currentOption.code}</span>}
        </span>
        <ChevronDown
          className={cn(
            "w-3 h-3 text-slate-400 transition-transform duration-200",
            isOpen && "rotate-180 text-blue-400"
          )}
        />
      </button>

      {isOpen && (
        <div
          role="listbox"
          className="absolute right-0 mt-1.5 w-52 rounded-xl bg-[#0F172A] border border-slate-700 shadow-2xl py-1.5 z-50 animate-in fade-in zoom-in-95 duration-150 backdrop-blur-xl"
        >
          <div className="px-3 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-400 border-b border-slate-800">
            Interface Language
          </div>
          <div className="max-h-64 overflow-y-auto py-1">
            {LANGUAGE_OPTIONS.map((opt) => {
              const isSelected = opt.code === currentLanguage;
              return (
                <button
                  key={opt.code}
                  type="button"
                  onClick={() => {
                    setLanguage(opt.code as SupportedLanguage);
                    setIsOpen(false);
                  }}
                  className={cn(
                    "w-full flex items-center justify-between px-3 py-2 text-xs transition-colors text-left",
                    isSelected
                      ? "bg-blue-600/15 text-blue-400 font-semibold"
                      : "text-slate-300 hover:bg-slate-800/80 hover:text-white"
                  )}
                >
                  <span className="flex items-center gap-2">
                    <span className="text-base">{opt.flag}</span>
                    <span>{opt.name}</span>
                    <span className="text-slate-500 text-[11px]">({opt.nativeName})</span>
                  </span>
                  {isSelected && <Check className="w-3.5 h-3.5 text-blue-400" />}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
