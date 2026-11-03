import React, { useState } from "react";
import { Eye, EyeOff, Lock } from "lucide-react";
import { cn } from "../../lib/utils";

interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

export const PasswordInput: React.FC<Props> = ({
  label,
  error,
  helperText,
  className,
  id,
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const inputId = id || `pwd_${label.toLowerCase().replace(/\s+/g, "_")}`;

  return (
    <div className="w-full space-y-1.5">
      <div className="flex items-center justify-between">
        <label htmlFor={inputId} className="block text-xs font-semibold text-slate-300">
          {label}
        </label>
        {helperText && <span className="text-[11px] text-slate-400">{helperText}</span>}
      </div>

      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
          <Lock className="w-4 h-4" />
        </div>

        <input
          id={inputId}
          type={showPassword ? "text" : "password"}
          className={cn(
            "w-full pl-9 pr-10 py-2.5 rounded-lg bg-slate-900/90 border text-white text-sm placeholder:text-slate-500 backdrop-blur-sm transition-all focus:outline-none focus:ring-2",
            error
              ? "border-red-500/70 focus:border-red-500 focus:ring-red-500/20"
              : "border-slate-800 focus:border-blue-500 focus:ring-blue-500/30",
            className
          )}
          {...props}
        />

        <button
          type="button"
          tabIndex={-1}
          onClick={() => setShowPassword((prev) => !prev)}
          className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-200 transition-colors focus:outline-none"
          aria-label={showPassword ? "Hide password" : "Show password"}
        >
          {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
        </button>
      </div>

      {error && (
        <p className="text-xs text-red-400 font-medium animate-in fade-in slide-in-from-top-1 duration-150">
          {error}
        </p>
      )}
    </div>
  );
};
