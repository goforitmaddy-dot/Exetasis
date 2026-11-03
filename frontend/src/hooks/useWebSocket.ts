import { useEffect } from "react";
import { MessageHandler, twinWs } from "../services/websocket";

export function useWebSocket(onMessage?: MessageHandler) {
  useEffect(() => {
    twinWs.connect();

    let unsubscribe: (() => void) | undefined;
    if (onMessage) {
      unsubscribe = twinWs.subscribe(onMessage);
    }

    return () => {
      if (unsubscribe) {
        unsubscribe();
      }
    };
  }, [onMessage]);

  return {
    send: (payload: Record<string, unknown>) => twinWs.send(payload),
  };
}
