"""WebSocket handler for text chat messages."""

import json
from aiohttp import web
from datetime import datetime
from typing import Set
from server.config import get_config
from server.storage import Storage
from server.auth import get_auth_manager
from server.utils.logger import get_logger
from common.protocol import ChatMessage


logger = get_logger(__name__)


# Global WebSocket connections per room
# Structure: {room_name: {websockets}}
TEXT_WEBSOCKETS: dict[str, Set[web.WebSocketResponse]] = {}


async def handle_text_websocket(request: web.Request) -> web.WebSocketResponse:
    """
    WebSocket handler for text chat.
    
    Accepts JSON messages in format:
    {
        "type": "text",
        "room": "general",
        "user": "username",
        "text": "message content",
        "timestamp": 1234567890.0
    }
    
    Broadcasts messages to all clients in the same room.
    """
    config = get_config()
    storage = Storage()
    
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    # Get room name from query params
    room = request.query.get("room", "general")
    
    # Add to room's WebSocket set
    if room not in TEXT_WEBSOCKETS:
        TEXT_WEBSOCKETS[room] = set()
    TEXT_WEBSOCKETS[room].add(ws)
    
    logger.info(f"[WS] New text chat connection in room '{room}'")
    
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    # Parse incoming message
                    data = json.loads(msg.data)
                    
                    # Extract message fields
                    user = data.get("user", "unknown")
                    text = data.get("text", "")
                    msg_type = data.get("type", "text")
                    timestamp = datetime.now().timestamp()
                    
                    # Create message object
                    message = ChatMessage(
                        type=msg_type,
                        room=room,
                        user=user,
                        text=text,
                        timestamp=timestamp
                    )
                    
                    # Broadcast to all clients in the room
                    disconnected = set()
                    for peer in TEXT_WEBSOCKETS.get(room, set()):
                        try:
                            if not peer.closed:
                                await peer.send_str(json.dumps(message.to_dict()))
                            else:
                                disconnected.add(peer)
                        except Exception as e:
                            logger.error(f"Error sending to peer: {e}")
                            disconnected.add(peer)
                    
                    # Remove disconnected WebSockets
                    for peer in disconnected:
                        TEXT_WEBSOCKETS[room].discard(peer)
                    
                    # Save message to database (optional, if user is authenticated)
                    # This would require extracting user_id from a token
                    logger.info(f"[WS] Message in '{room}' from '{user}': {text[:50]}")
                
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received: {msg.data}")
                    await ws.send_str(json.dumps({
                        'type': 'error',
                        'message': 'Invalid JSON'
                    }))
            
            elif msg.type == web.WSMsgType.ERROR:
                logger.error(f"WebSocket error: {ws.exception()}")
                break
    
    except Exception as e:
        logger.error(f"WebSocket error in room '{room}': {e}")
    
    finally:
        # Remove from room on disconnect
        TEXT_WEBSOCKETS[room].discard(ws)
        logger.info(f"[WS] Disconnected from room '{room}'")
    
    return ws


async def get_room_stats() -> dict:
    """Get statistics about active rooms."""
    return {
        room: len(sockets)
        for room, sockets in TEXT_WEBSOCKETS.items()
        if sockets
    }

