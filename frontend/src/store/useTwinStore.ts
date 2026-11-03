import { create } from "zustand";
import { DigitalTwinNode, TwinNodeStatus, ZoneClusterData } from "../types";

interface TwinStoreState {
  nodes: DigitalTwinNode[];
  zones: ZoneClusterData[];
  selectedNodeId: string | null;
  officeName: string;
  isLoading: boolean;
  setSnapshot: (nodes: DigitalTwinNode[], zones: ZoneClusterData[], officeName: string) => void;
  selectNode: (id: string | null) => void;
  updateNodeStatus: (id: string, status: TwinNodeStatus, delta?: Record<string, unknown>) => void;
  setLoading: (loading: boolean) => void;
}

export const useTwinStore = create<TwinStoreState>((set) => ({
  nodes: [],
  zones: [],
  selectedNodeId: null,
  officeName: "HQ - Digital Twin",
  isLoading: false,

  setSnapshot: (nodes, zones, officeName) =>
    set({ nodes, zones, officeName, isLoading: false }),

  selectNode: (id) => set({ selectedNodeId: id }),

  updateNodeStatus: (id, status, delta = {}) =>
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === id
          ? {
              ...node,
              status,
              state_metadata: { ...node.state_metadata, ...delta },
            }
          : node
      ),
    })),

  setLoading: (loading) => set({ isLoading: loading }),
}));
