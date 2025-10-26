"""WebRTC signaling for voice chat."""

import json
from aiohttp import web
from typing import Set
from server.utils.logger import get_logger


logger = get_logger(__name__)


# WebSocket connections for signaling
SIGNALING_WEBSOCKETS: dict[str, Set[web.WebSocketResponse]] = {}


async def handle_signaling_websocket(request: web.Request) -> web.WebSocketResponse:
    """
    WebSocket handler for WebRTC signaling.
    
    Handles SDP offers/answers and ICE candidates for voice chat.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    room = request.query.get("room", "general")
    
    if room not in SIGNALING_WEBSOCKETS:
        SIGNALING_WEBSOCKETS[room] = set()
    SIGNALING_WEBSOCKETS[room].add(ws)
    
    logger.info(f"[Signaling] New connection in room '{room}'")
    
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    # Parse signaling message
                    data = json.loads(msg.data)
                    
                    # Broadcast signaling message to other peers in the room
                    for peer in list(SIGNALING_WEBSOCKETS.get(room, set())):
                        if peer != ws and not peer.closed:
                            try:
                                await peer.send_str(msg.data)
                            except Exception as e:
                                logger.error(f"Error forwarding signal: {e}")
                
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in signaling message")
    
    except Exception as e:
        logger.error(f"Signaling error in room '{room}': {e}")
    
    finally:
        SIGNALING_WEBSOCKETS[room].discard(ws)
        logger.info(f"[Signaling] Disconnected from room '{room}'")
    
    return ws

