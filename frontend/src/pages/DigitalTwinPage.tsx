import React from "react";
import { DigitalTwinCanvas } from "../digital-twin/Canvas";
import { EmployeeDirectory } from "../features/employees/EmployeeDirectory";
import { useTwinStore } from "../store/useTwinStore";
import { StatusBadge } from "../components/StatusBadge";
import { Maximize2 } from "lucide-react";

export const DigitalTwinPage: React.FC = () => {
  const { nodes, selectedNodeId, officeName } = useTwinStore();
  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">3D Digital Twin Visualization</h2>
          <p className="text-xs text-slate-400">{officeName} — Spatial Layout & Real-time Nodes</p>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <Maximize2 className="w-4 h-4" />
          <span>Orbit: Left-Click + Drag | Pan: Right-Click | Zoom: Scroll</span>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-4 min-h-0">
        {/* 3D WebGL Canvas Container */}
        <div className="lg:col-span-3 rounded-xl overflow-hidden border border-slate-800 shadow-2xl relative">
          <DigitalTwinCanvas />

          {/* Selected Node Float Overlay */}
          {selectedNode && (
            <div className="absolute top-4 left-4 bg-slate-900/90 border border-slate-700/80 backdrop-blur-md p-4 rounded-xl shadow-xl w-72 text-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-white">{selectedNode.label}</span>
                <StatusBadge status={selectedNode.status} />
              </div>
              <div className="text-slate-400">
                Type: <span className="text-slate-200 capitalize">{selectedNode.node_type}</span>
              </div>
              <div className="text-slate-400">
                Coordinates: ({selectedNode.position.x}, {selectedNode.position.y}, {selectedNode.position.z})
              </div>
              {selectedNode.state_metadata && (
                <pre className="text-[10px] bg-slate-950 p-2 rounded text-slate-300 font-mono overflow-x-auto">
                  {JSON.stringify(selectedNode.state_metadata, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>

        {/* Sidebar Directory and Zone List */}
        <div className="flex flex-col gap-4 overflow-y-auto">
          <EmployeeDirectory />
        </div>
      </div>
    </div>
  );
};
