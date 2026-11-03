import React from "react";
import { Users } from "lucide-react";
import { useTwinStore } from "../../store/useTwinStore";
import { StatusBadge } from "../../components/StatusBadge";

export const EmployeeDirectory: React.FC = () => {
  const { nodes, selectedNodeId, selectNode } = useTwinStore();

  return (
    <div className="bg-[#111827] border border-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <Users className="w-5 h-5 text-blue-400" />
        <h3 className="text-sm font-bold text-white uppercase tracking-wider">Spatial Workforce Directory [STUB]</h3>
      </div>

      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
        {nodes.map((node) => {
          const isSelected = selectedNodeId === node.id;
          return (
            <div
              key={node.id}
              onClick={() => selectNode(node.id)}
              className={`p-3 rounded-lg border text-xs cursor-pointer flex items-center justify-between transition-colors ${
                isSelected
                  ? "bg-blue-600/10 border-blue-500/30 text-white"
                  : "bg-slate-900/60 border-slate-800/80 text-slate-300 hover:bg-slate-900"
              }`}
            >
              <div>
                <div className="font-semibold">{node.label}</div>
                <div className="text-[11px] text-slate-500 capitalize">{node.node_type}</div>
              </div>
              <StatusBadge status={node.status} />
            </div>
          );
        })}
      </div>
    </div>
  );
};
