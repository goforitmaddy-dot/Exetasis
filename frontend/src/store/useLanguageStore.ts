import { create } from "zustand";

import en from "../locales/en.json";
import hi from "../locales/hi.json";
import fr from "../locales/fr.json";
import es from "../locales/es.json";
import de from "../locales/de.json";
import ja from "../locales/ja.json";
import pa from "../locales/pa.json";

export type SupportedLanguage = "en" | "hi" | "fr" | "es" | "de" | "ja" | "pa";

export interface LanguageOption {
  code: SupportedLanguage;
  name: string;
  nativeName: string;
  flag: string;
}

export const LANGUAGE_OPTIONS: LanguageOption[] = [
  { code: "en", name: "English", nativeName: "English", flag: "🇺🇸" },
  { code: "hi", name: "Hindi", nativeName: "हिन्दी", flag: "🇮🇳" },
  { code: "pa", name: "Punjabi", nativeName: "ਪੰਜਾਬੀ", flag: "🇮🇳" },
  { code: "fr", name: "French", nativeName: "Français", flag: "🇫🇷" },
  { code: "es", name: "Spanish", nativeName: "Español", flag: "🇪🇸" },
  { code: "de", name: "German", nativeName: "Deutsch", flag: "🇩🇪" },
  { code: "ja", name: "Japanese", nativeName: "日本語", flag: "🇯🇵" },
];

const translations: Record<SupportedLanguage, Record<string, unknown>> = {
  en,
  hi,
  fr,
  es,
  de,
  ja,
  pa,
};

function getNestedValue(obj: Record<string, unknown>, path: string): string | undefined {
  const parts = path.split(".");
  let current: unknown = obj;
  for (const part of parts) {
    if (current && typeof current === "object" && part in current) {
      current = (current as Record<string, unknown>)[part];
    } else {
      return undefined;
    }
  }
  return typeof current === "string" ? current : undefined;
}

interface LanguageState {
  currentLanguage: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => void;
  t: (path: string, fallback?: string) => string;
}

const STORAGE_KEY = "exetasis_preferred_language";

export const useLanguageStore = create<LanguageState>((set, get) => {
  const initialLang: SupportedLanguage = (() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY) as SupportedLanguage | null;
      if (saved && saved in translations) {
        return saved;
      }
    } catch {
      // LocalStorage unavailable
    }
    return "en";
  })();

  return {
    currentLanguage: initialLang,

    setLanguage: (lang: SupportedLanguage) => {
      try {
        localStorage.setItem(STORAGE_KEY, lang);
      } catch {
        // LocalStorage unavailable
      }
      set({ currentLanguage: lang });
    },

    t: (path: string, fallback?: string): string => {
      const { currentLanguage } = get();
      const currentDict = translations[currentLanguage] || translations.en;
      const translated = getNestedValue(currentDict, path);
      if (translated) return translated;

      // Fallback to English
      const enTranslated = getNestedValue(translations.en, path);
      if (enTranslated) return enTranslated;

      return fallback || path;
    },
  };
});
