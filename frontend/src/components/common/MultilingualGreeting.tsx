import React, { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";

interface GreetingItem {
  greeting: string;
  language: string;
  script?: string;
}

const GREETINGS: GreetingItem[] = [
  { greeting: "Hello", language: "English" },
  { greeting: "नमस्ते", language: "Hindi (हिन्दी)" },
  { greeting: "Bonjour", language: "French (Français)" },
  { greeting: "Hola", language: "Spanish (Español)" },
  { greeting: "こんにちは", language: "Japanese (日本語)" },
  { greeting: "مرحباً", language: "Arabic (العربية)" },
  { greeting: "Ciao", language: "Italian (Italiano)" },
  { greeting: "Guten Tag", language: "German (Deutsch)" },
  { greeting: "Olá", language: "Portuguese (Português)" },
  { greeting: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", language: "Punjabi (ਪੰਜਾਬੀ)" },
];

export const MultilingualGreeting: React.FC = () => {
  const [index, setIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setInterval(() => {
      // Trigger fade out
      setIsVisible(false);
      setTimeout(() => {
        setIndex((prev) => (prev + 1) % GREETINGS.length);
        setIsVisible(true);
      }, 350); // duration of exit animation
    }, 2800);

    return () => clearInterval(timer);
  }, []);

  const current = GREETINGS[index];

  return (
    <div
      aria-live="polite"
      className="inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-slate-900/80 border border-slate-700/80 backdrop-blur-md shadow-lg shadow-blue-900/10"
    >
      <div className="flex items-center justify-center w-5 h-5 rounded-full bg-blue-500/20 text-blue-400">
        <Sparkles className="w-3 h-3 animate-spin" style={{ animationDuration: "6s" }} />
      </div>

      <div className="flex items-center gap-2 min-w-[170px]">
        {/* Animated Greeting Text */}
        <span
          className={`font-semibold text-sm text-white tracking-wide transition-all duration-300 transform ${
            isVisible
              ? "opacity-100 translate-y-0 filter-none"
              : "opacity-0 -translate-y-2 blur-[2px]"
          }`}
        >
          {current.greeting}
        </span>

        {/* Language Origin Subtext */}
        <span
          className={`text-[11px] font-medium text-slate-400 transition-opacity duration-300 ${
            isVisible ? "opacity-100" : "opacity-0"
          }`}
        >
          • {current.language}
        </span>
      </div>
    </div>
  );
};
