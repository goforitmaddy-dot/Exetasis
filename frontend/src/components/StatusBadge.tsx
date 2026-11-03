import React from "react";
import { cn } from "../lib/utils";
import { TwinNodeStatus } from "../types";

interface Props {
  status: TwinNodeStatus | string;
  className?: string;
}

export const StatusBadge: React.FC<Props> = ({ status, className }) => {
  const normalized = status.toLowerCase();

  const styles: Record<string, string> = {
    active: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    focused: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    collaborating: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    alert: "bg-red-500/10 text-red-400 border-red-500/20",
    idle: "bg-slate-500/10 text-slate-400 border-slate-500/20",
  };

  const currentStyle = styles[normalized] || styles.idle;

  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border capitalize",
        currentStyle,
        className
      )}
    >
      <span className="w-1.5 h-1.5 rounded-full mr-1.5 bg-current" />
      {status}
    </span>
  );
};
