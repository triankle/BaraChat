
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
                    "type": data.get("type", "text"),
                    "room": room,
                    "user": data.get("user", "unknown"),
                    "text": data.get("text", ""),
                    "timestamp": time.time(),
                }
                
                # Add file info if it's a file message
                if data.get("type") == "file":
                    payload["file_info"] = data.get("file_info", {})

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
# 🔹 Voice signaling WebSocket handler
SIGNALING_ROOMS = {}

async def handle_voice_signaling(request):
    """
    WebSocket handler for WebRTC voice signaling.
    Handles SDP offers/answers and ICE candidates.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    room = request.query.get("room", "general")
    
    if room not in SIGNALING_ROOMS:
        SIGNALING_ROOMS[room] = set()
    SIGNALING_ROOMS[room].add(ws)
    
    print(f"[Voice] New signaling connection in room '{room}'")
    
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # Broadcast signaling message to other peers in room
                for peer in list(SIGNALING_ROOMS.get(room, set())):
                    if peer != ws and not peer.closed:
                        try:
                            await peer.send_str(msg.data)
                        except Exception as e:
                            print(f"[Voice] Error forwarding signal: {e}")
    
    finally:
        SIGNALING_ROOMS[room].discard(ws)
        print(f"[Voice] Disconnected from room '{room}'")
    
    return ws


# -------------------------------
# 🔹 Simple HTTP route to test if the server is running
async def handle_root(request):
    return web.Response(text="LocalCord Server Active ✅")


# -------------------------------
# 🔹 Main function that starts the server
# Simple in-memory file storage
UPLOADED_FILES = {}  # {filename: (content, mime_type)}

async def handle_upload(request):
    """Handle file upload."""
    data = await request.post()
    file_obj = data.get('file')
    room = data.get('room', 'general')
    
    if not file_obj:
        return web.json_response({'error': 'No file provided'}, status=400)
    
    filename = file_obj.filename
    file_content = file_obj.file.read()
    
    # Store file
    UPLOADED_FILES[filename] = (file_content, file_obj.content_type or 'application/octet-stream')
    
    file_url = f"/download/{filename}"
    
    print(f"[Upload] File uploaded: {filename} ({len(file_content)} bytes) in room '{room}'")
    
    return web.json_response({
        'success': True,
        'file_url': file_url,
        'filename': filename,
        'file_size': len(file_content)
    })

async def handle_download(request):
    """Handle file download."""
    from urllib.parse import unquote
    
    filename = request.match_info.get('filename')
    
    # Decode URL-encoded filename
    decoded_filename = unquote(filename)
    
    # Try both encoded and decoded versions
    file_key = None
    if decoded_filename in UPLOADED_FILES:
        file_key = decoded_filename
    elif filename in UPLOADED_FILES:
        file_key = filename
    
    if not file_key:
        print(f"[Download] File not found: {decoded_filename}")
        return web.json_response({'error': 'File not found'}, status=404)
    
    content, mime_type = UPLOADED_FILES[file_key]
    
    print(f"[Download] Serving file: {file_key} ({len(content)} bytes)")
    
    return web.Response(
        body=content,
        content_type=mime_type,
        headers={
            'Content-Disposition': f'attachment; filename="{file_key}"'
        }
    )

def create_app():
    app = web.Application()               # Creates the aiohttp application
    app.router.add_get("/", handle_root)  # GET route for /
    app.router.add_get("/ws", handle_ws)  # GET route for text chat WebSocket
    app.router.add_get("/voice", handle_voice_signaling)  # GET route for voice signaling
    app.router.add_post("/api/upload", handle_upload)  # POST route for file upload
    app.router.add_get("/download/{filename}", handle_download)  # GET route for file download
    return app


# -------------------------------
# 🔹 Main entry point of the script
if __name__ == "__main__":
    app = create_app()                      # builds the application
    web.run_app(app, host="127.0.0.1", port=8765)  # starts the local server
    # ⚙️ server listens on http://127.0.0.1:8765/
