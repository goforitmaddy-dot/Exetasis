import React from "react";
import { Html } from "@react-three/drei";
import { ZoneClusterData } from "../types";

interface Props {
  zone: ZoneClusterData;
}

export const ZoneCluster: React.FC<Props> = ({ zone }) => {
  const width = Math.abs(zone.bounds.max_x - zone.bounds.min_x);
  const depth = Math.abs(zone.bounds.max_z - zone.bounds.min_z);
  const centerX = (zone.bounds.min_x + zone.bounds.max_x) / 2;
  const centerZ = (zone.bounds.min_z + zone.bounds.max_z) / 2;

  return (
    <group position={[centerX, 0.02, centerZ]}>
      {/* Zone Floor Perimeter Plane */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <planeGeometry args={[width, depth]} />
        <meshBasicMaterial
          color={zone.color}
          transparent
          opacity={0.12}
          depthWrite={false}
        />
      </mesh>

      {/* Zone Label Floating in 3D */}
      <Html position={[0, 0.1, -depth / 2 + 0.5]} center distanceFactor={16}>
        <div
          className="px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider text-slate-300 pointer-events-none border border-slate-700/60 bg-slate-900/60 backdrop-blur-sm"
          style={{ borderColor: zone.color }}
        >
          {zone.name}
        </div>
      </Html>
    </group>
  );
};
