import React from "react";
import { Grid } from "@react-three/drei";
import { useTwinStore } from "../store/useTwinStore";
import { EmployeeAvatar } from "./EmployeeAvatar";
import { ZoneCluster } from "./ZoneCluster";

export const OfficeScene: React.FC = () => {
  const { nodes, zones, selectNode } = useTwinStore();

  return (
    <group
      onPointerMissed={(e) => {
        if (e.type === "click") {
          selectNode(null);
        }
      }}
    >
      {/* Subtle Lighting */}
      <ambientLight intensity={0.65} />
      <directionalLight
        position={[10, 15, 10]}
        intensity={1.2}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <pointLight position={[-10, 8, -10]} intensity={0.4} color="#60A5FA" />

      {/* Grid Floor */}
      <Grid
        args={[30, 30]}
        cellSize={1}
        cellThickness={0.6}
        cellColor="#1E293B"
        sectionSize={5}
        sectionThickness={1.2}
        sectionColor="#334155"
        fadeDistance={25}
        fadeStrength={1}
      />

      {/* Department Zones */}
      {zones.map((zone) => (
        <ZoneCluster key={zone.id} zone={zone} />
      ))}

      {/* Nodes & Avatars */}
      {nodes.map((node) => (
        <EmployeeAvatar key={node.id} node={node} />
      ))}
    </group>
  );
};
