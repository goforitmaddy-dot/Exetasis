import React from "react";
import { cn } from "../lib/utils";

interface Props {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: string;
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<Props> = ({
  title,
  value,
  subtitle,
  trend,
  icon,
  className,
}) => {
  return (
    <div
      className={cn(
        "bg-[#111827] border border-slate-800 rounded-xl p-5 flex flex-col justify-between shadow-sm hover:border-slate-700 transition-colors",
        className
      )}
    >
      <div className="flex items-center justify-between text-slate-400 mb-2">
        <span className="text-sm font-medium">{title}</span>
        {icon && <span className="text-slate-400">{icon}</span>}
      </div>
      <div>
        <div className="text-2xl font-bold tracking-tight text-white">{value}</div>
        {(subtitle || trend) && (
          <div className="mt-1 flex items-center gap-2 text-xs text-slate-400">
            {trend && <span className="text-emerald-400 font-medium">{trend}</span>}
            {subtitle && <span>{subtitle}</span>}
          </div>
        )}
      </div>
    </div>
  );
};
