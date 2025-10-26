
# ===============================
# This file contains a small local chat server using aiohttp.
# Aiohttp is an async HTTP client-server framework in Python based on Python's async I/O library asyncio
# It handles WebSocket connections, broadcasts messages to all connected clients,
# and listens on port 8765 (localhost only by default).
# ===============================
import asyncio    # pyright: ignore[reportUnusedImport]
import json
from aiohttp import web  # async web framework

# -------------------------------
# 🔸 Global dictionary that keeps the list of WebSockets by "room"
# Structure : { "room_name": set(websockets) }
ROOMS = {}

# -------------------------------
# 🔹 Main WebSocket handling function
async def handle_ws(request):
    """
    This function is called when a client connects to /ws.
    It handles receiving and broadcasting messages.
    """
    ws = web.WebSocketResponse()   # creates a WebSocket object for this connection
    await ws.prepare(request)      # establishes the WS connection on the server side

    # Gets the room name from the URL parameters (ex: ?room=general)
    room = request.query.get("room", "general")

    # Adds the WS to the list of connections for this room
    ROOMS.setdefault(room, set()).add(ws)

    print(f"[+] New connection in room '{room}'")

    # Main receiving loop
    try:
        async for msg in ws:
            # If we receive a text message (non-binary)
            if msg.type == web.WSMsgType.TEXT:
                # Converts the received JSON text to a Python object
                data = json.loads(msg.data)

                # Prepares an output message to broadcast to everyone
                import time
                payload = {
                    "type": "text",
                    "room": room,
                    "user": data.get("user", "unknown"),
                    "text": data.get("text", ""),
                    "timestamp": time.time(),
                }

                # Sends this message to all clients connected to the same room
                for peer in list(ROOMS[room]):
                    if not peer.closed:
                        await peer.send_str(json.dumps(payload))

            elif msg.type == web.WSMsgType.ERROR:
                print(f"[!] WS Error : {ws.exception()}")

    finally:
        # When the client disconnects, we remove them from the room
        ROOMS[room].discard(ws)
        print(f"[-] Disconnection from room '{room}'")

    return ws  # We return the WebSocketResponse (required for aiohttp)


# -------------------------------
# 🔹 Simple HTTP route to test if the server is running
async def handle_root(request):
    return web.Response(text="LocalCord Server Active ✅")


# -------------------------------
# 🔹 Main function that starts the server
def create_app():
    app = web.Application()               # Creates the aiohttp application
    app.router.add_get("/", handle_root)  # GET route for /
    app.router.add_get("/ws", handle_ws)  # GET route for the WebSocket
    return app


# -------------------------------
# 🔹 Main entry point of the script
if __name__ == "__main__":
    app = create_app()                      # builds the application
    web.run_app(app, host="127.0.0.1", port=8765)  # starts the local server
    # ⚙️ server listens on http://127.0.0.1:8765/
