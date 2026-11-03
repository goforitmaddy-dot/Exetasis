from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.app.core.logging import logger
from backend.app.websocket.connection_manager import manager

ws_router = APIRouter()


@ws_router.websocket("/ws/digital-twin")
async def digital_twin_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint streaming real-time digital twin state and event pulses."""
    await manager.connect(websocket)
    try:
        # Send initial welcome / sync event
        await websocket.send_json({
            "event_type": "pong",
            "delta": {"message": "Connected to Exetasis Digital Twin stream"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        while True:
            data = await websocket.receive_json()
            action = data.get("action", "ping")

            if action == "ping":
                await websocket.send_json({
                    "event_type": "pong",
                    "delta": {"status": "alive"},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            elif action == "focus_node":
                node_id = data.get("node_id")
                logger.debug("Client requested focus on node: %s", node_id)
                await websocket.send_json({
                    "event_type": "node_update",
                    "node_id": node_id,
                    "delta": {"focused": True},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            else:
                await websocket.send_json({
                    "event_type": "pong",
                    "delta": {"echo_action": action},
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error("WebSocket exception: %s", e)
        manager.disconnect(websocket)
