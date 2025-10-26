"""Data models using SQLModel ORM."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(SQLModel, table=True):
    """User model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: Optional[str] = None
    password_hash: str  # bcrypt hash
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    last_seen: Optional[datetime] = None
    public_key: Optional[str] = None  # For E2EE


class Message(SQLModel, table=True):
    """Chat message model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    room: str = Field(index=True)
    user_id: int = Field(foreign_key="user.id")
    username: str  # Denormalized for quick access
    content: str
    message_type: str = "text"  # text, file, system
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.now, index=True)
    is_encrypted: bool = False


class Room(SQLModel, table=True):
    """Room/Channel model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    is_private: bool = False
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    member_count: int = 0


class File(SQLModel, table=True):
    """Uploaded file model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploader_id: int = Field(foreign_key="user.id")
    uploader_username: str
    room: str
    uploaded_at: datetime = Field(default_factory=datetime.now)
    is_encrypted: bool = False

