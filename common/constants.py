"""Constants used throughout the application."""

# Network constants
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_WS_PORT = 8765

# Message types for WebSocket protocol
class WSMsgType:
    """WebSocket message types."""
    TEXT = "text"
    FILE = "file"
    VOICE_DATA = "voice_data"
    SIGNALING = "signaling"
    ERROR = "error"
    HEARTBEAT = "heartbeat"

# HTTP routes
class Routes:
    """HTTP API routes."""
    ROOT = "/"
    WS = "/ws"
    API = "/api"
    UPLOAD = "/api/upload"
    DOWNLOAD = "/api/download"
    USER_INFO = "/api/user"
    HEALTH = "/health"

# Database constants
DB_NAME = "barachat.db"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
UPLOAD_DIR = "uploads"

# Crypto constants
KEY_SIZE = 32  # 256 bits for encryption keys
SALT_SIZE = 16  # 128 bits for salt

# User limits
MAX_USERNAME_LENGTH = 32
MAX_ROOM_NAME_LENGTH = 64

