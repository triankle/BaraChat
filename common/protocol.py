"""Protocol definitions for JSON message schemas."""

from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict
from enum import Enum


class MessageType(Enum):
    """Types of messages in the chat system."""
    TEXT = "text"
    FILE = "file"
    SYSTEM = "system"
    VOICE_START = "voice_start"
    VOICE_END = "voice_end"
    TYPING = "typing"


@dataclass
class ChatMessage:
    """Chat message structure."""
    type: str
    room: str
    user: str
    text: str
    timestamp: Optional[float] = None
    file_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        # Remove None values for cleaner JSON
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class FileUploadResponse:
    """Response for file upload."""
    success: bool
    file_url: str
    file_name: str
    file_size: int
    message: Optional[str] = None


@dataclass
class SignalingMessage:
    """WebRTC signaling message."""
    type: str  # "offer", "answer", "ice_candidate"
    room: str
    user: str
    data: Dict[str, Any]  # SDP or ICE candidate info


@dataclass
class UserInfo:
    """User information."""
    username: str
    is_online: bool
    current_room: Optional[str] = None


def parse_message(json_str: str) -> Optional[ChatMessage]:
    """Parse JSON string to ChatMessage."""
    import json
    try:
        data = json.loads(json_str)
        return ChatMessage(**data)
    except (json.JSONDecodeError, TypeError, KeyError):
        return None

