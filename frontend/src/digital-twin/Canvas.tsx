import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { OfficeScene } from "./OfficeScene";

export const DigitalTwinCanvas: React.FC = () => {
  return (
    <div className="w-full h-full relative bg-[#090D16]">
      <Canvas
        camera={{ position: [0, 12, 16], fov: 45 }}
        shadows
        gl={{ antialias: true }}
      >
        <OrbitControls
          makeDefault
          maxPolarAngle={Math.PI / 2.1}
          minDistance={5}
          maxDistance={35}
          dampingFactor={0.05}
        />
        <OfficeScene />
      </Canvas>
    </div>
  );
};
