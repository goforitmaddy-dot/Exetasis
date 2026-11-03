import { useEffect } from "react";
import { api } from "../services/api";
import { useTwinStore } from "../store/useTwinStore";
import { useWebSocket } from "./useWebSocket";

export function useDigitalTwin() {
  const { setSnapshot, updateNodeStatus, setLoading } = useTwinStore();

  useWebSocket((msg) => {
    if (msg.event_type === "node_update" && msg.node_id) {
      updateNodeStatus(
        msg.node_id,
        "active",
        msg.delta
      );
    }
  });

  useEffect(() => {
    let mounted = true;
    setLoading(true);

    api
      .getDigitalTwinState()
      .then((data) => {
        if (mounted) {
          setSnapshot(data.nodes, data.zones, data.office_name);
        }
      })
      .catch((err) => {
        console.error("Failed to fetch initial digital twin state:", err);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [setSnapshot, setLoading]);
}
