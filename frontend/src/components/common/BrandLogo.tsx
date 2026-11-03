import React from "react";
import { Link } from "react-router-dom";
import { cn } from "../../lib/utils";

interface Props {
  className?: string;
  size?: "sm" | "md" | "lg";
  withLink?: boolean;
}

export const BrandLogo: React.FC<Props> = ({ className, size = "md", withLink = true }) => {
  const sizeClasses = {
    sm: "text-base gap-2",
    md: "text-lg gap-2.5",
    lg: "text-2xl gap-3",
  };

  const iconSizes = {
    sm: "w-6 h-6",
    md: "w-8 h-8",
    lg: "w-10 h-10",
  };

  const content = (
    <div className={cn("inline-flex items-center group font-sans tracking-tight", sizeClasses[size], className)}>
      {/* Brand Icon: Living Spatial Intelligent Node */}
      <div
        className={cn(
          "relative flex items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 via-indigo-600 to-violet-700 p-0.5 shadow-lg shadow-blue-500/20 group-hover:shadow-blue-500/40 transition-all duration-300",
          iconSizes[size]
        )}
      >
        <div className="w-full h-full bg-[#0B1020] rounded-[10px] flex items-center justify-center relative overflow-hidden">
          {/* Subtle Ambient Pulse */}
          <div className="absolute inset-0 bg-blue-500/10 group-hover:bg-blue-500/20 transition-colors" />

          {/* Abstract Geometric Tri-Node / Delta Mark */}
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-4/5 h-4/5 text-white"
          >
            <path
              d="M12 3L20 8V16L12 21L4 16V8L12 3Z"
              stroke="url(#exetasis-gradient)"
              strokeWidth="1.8"
              strokeLinejoin="round"
            />
            <circle cx="12" cy="12" r="2.5" fill="#60A5FA" />
            <path
              d="M12 4.5V9.5M18.5 15L14 13M5.5 15L10 13"
              stroke="#818CF8"
              strokeWidth="1.2"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="exetasis-gradient" x1="4" y1="3" x2="20" y2="21" gradientUnits="userSpaceOnUse">
                <stop stopColor="#60A5FA" />
                <stop offset="0.5" stopColor="#818CF8" />
                <stop offset="1" stopColor="#C084FC" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>

      {/* Brand Typography */}
      <div className="flex flex-col leading-none">
        <span className="font-extrabold tracking-widest uppercase text-white font-mono flex items-center gap-1.5">
          EXETASIS
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" />
        </span>
        {size !== "sm" && (
          <span className="text-[9px] tracking-widest uppercase font-semibold text-slate-400 mt-0.5">
            Workplace Intelligence
          </span>
        )}
      </div>
    </div>
  );

  if (withLink) {
    return (
      <Link to="/" className="outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded-lg">
        {content}
      </Link>
    );
  }

  return content;
};
