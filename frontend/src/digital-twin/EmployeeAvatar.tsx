import React, { useRef, useState } from "react";
import { Mesh } from "three";
import { Html } from "@react-three/drei";
import { DigitalTwinNode, TwinNodeStatus } from "../types";
import { useTwinStore } from "../store/useTwinStore";

interface Props {
  node: DigitalTwinNode;
}

const STATUS_COLORS: Record<TwinNodeStatus, string> = {
  active: "#10B981",       // emerald
  focused: "#3B82F6",      // blue
  collaborating: "#8B5CF6",// purple
  alert: "#EF4444",        // red
  idle: "#6B7280",         // slate
};

export const EmployeeAvatar: React.FC<Props> = ({ node }) => {
  const meshRef = useRef<Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const { selectedNodeId, selectNode } = useTwinStore();

  const isSelected = selectedNodeId === node.id;
  const color = STATUS_COLORS[node.status] || "#6B7280";

  return (
    <group position={[node.position.x, node.position.y, node.position.z]}>
      {/* Node Base / Desk Platform */}
      <mesh
        position={[0, 0, 0]}
        castShadow
        receiveShadow
        onClick={(e) => {
          e.stopPropagation();
          selectNode(node.id);
        }}
        onPointerOver={(e) => {
          e.stopPropagation();
          setHovered(true);
        }}
        onPointerOut={() => setHovered(false)}
      >
        <boxGeometry args={[1.2, 0.4, 0.8]} />
        <meshStandardMaterial
          color={isSelected ? "#60A5FA" : hovered ? "#374151" : "#1F2937"}
          roughness={0.4}
        />
      </mesh>

      {/* Avatar Indicator Sphere */}
      <mesh ref={meshRef} position={[0, 0.6, 0]} castShadow>
        <sphereGeometry args={[0.25, 24, 24]} />
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={isSelected || hovered ? 0.6 : 0.2}
          roughness={0.2}
        />
      </mesh>

      {/* Label & Status Billboard Tooltip */}
      {(hovered || isSelected) && (
        <Html position={[0, 1.1, 0]} center distanceFactor={12}>
          <div className="bg-slate-900/90 border border-slate-700 backdrop-blur-md px-2.5 py-1.5 rounded shadow-xl text-xs whitespace-nowrap pointer-events-none text-slate-100 flex flex-col gap-0.5">
            <span className="font-semibold">{node.label}</span>
            <span className="text-[10px] text-slate-400 capitalize">
              Status: <span style={{ color }}>{node.status}</span>
            </span>
          </div>
        </Html>
      )}
    </group>
  );
};
