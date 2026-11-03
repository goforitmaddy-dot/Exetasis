import React, { useState } from "react";
import { cn } from "../../lib/utils";

interface Props {
  onClick?: () => void;
  className?: string;
  label?: string;
}

export const SocialLoginButton: React.FC<Props> = ({
  onClick,
  className,
  label = "Continue with Google",
}) => {
  const [showToast, setShowToast] = useState(false);

  const handleClick = () => {
    if (onClick) {
      onClick();
    } else {
      setShowToast(true);
      setTimeout(() => setShowToast(false), 2400);
    }
  };

  return (
    <div className="relative w-full">
      <button
        type="button"
        onClick={handleClick}
        className={cn(
          "w-full flex items-center justify-center gap-3 py-2.5 px-4 rounded-lg bg-slate-900 border border-slate-700/80 hover:bg-slate-800/90 hover:border-slate-600 text-slate-200 text-sm font-medium transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-400/20 active:scale-[0.99]",
          className
        )}
      >
        {/* Google Multi-Color SVG Icon */}
        <svg className="w-4 h-4 flex-shrink-0" viewBox="0 0 24 24">
          <path
            fill="#4285F4"
            d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.65v3.05h3.9c2.28-2.1 3.645-5.18 3.645-9.14z"
          />
          <path
            fill="#34A853"
            d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.9-3.05c-1.08.72-2.45 1.16-4.03 1.16-3.1 0-5.74-2.1-6.68-4.92H1.21v3.15C3.25 21.43 7.33 24 12 24z"
          />
          <path
            fill="#FBBC05"
            d="M5.32 14.28c-.24-.73-.38-1.5-.38-2.28s.14-1.55.38-2.28V6.57H1.21C.44 8.11 0 9.99 0 12s.44 3.89 1.21 5.43l4.11-3.15z"
          />
          <path
            fill="#EA4335"
            d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.25 2.57 1.21 6.57l4.11 3.15c.94-2.82 3.58-4.97 6.68-4.97z"
          />
        </svg>
        <span>{label}</span>
      </button>

      {/* Non-functional placeholder feedback tooltip */}
      {showToast && (
        <div className="absolute -top-10 left-1/2 -translate-x-1/2 px-3 py-1 bg-slate-800 text-slate-300 text-xs rounded shadow-lg border border-slate-700 whitespace-nowrap animate-in fade-in duration-150 z-20">
          Google SSO is a mock placeholder for this preview
        </div>
      )}
    </div>
  );
};
