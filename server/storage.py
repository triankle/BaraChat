"""Database storage and file handling."""

import aiofiles
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session, select
from server.models import User, Message, Room, File, UserRole
from server.config import get_config


class Storage:
    """Database and file storage manager."""
    
    def __init__(self):
        self.config = get_config()
        self.engine = create_engine(f"sqlite:///{self.config.db_path}")
        self._initialized = False
    
    def initialize(self):
        """Initialize database tables."""
        if not self._initialized:
            SQLModel.metadata.create_all(self.engine)
            self._initialized = True
    
    def get_session(self) -> Session:
        """Get a database session."""
        return Session(self.engine)
    
    # User operations
    def create_user(self, username: str, password_hash: str, 
                   email: Optional[str] = None) -> User:
        """Create a new user."""
        with self.get_session() as session:
            user = User(
                username=username,
                password_hash=password_hash,
                email=email,
                role=UserRole.USER
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        with self.get_session() as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        with self.get_session() as session:
            return session.get(User, user_id)
    
    # Message operations
    def save_message(self, room: str, user_id: int, username: str, 
                    content: str, message_type: str = "text",
                    file_url: Optional[str] = None,
                    file_size: Optional[int] = None) -> Message:
        """Save a message to the database."""
        with self.get_session() as session:
            message = Message(
                room=room,
                user_id=user_id,
                username=username,
                content=content,
                message_type=message_type,
                file_url=file_url,
                file_size=file_size
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message
    
    def get_recent_messages(self, room: str, limit: int = 50) -> List[Message]:
        """Get recent messages for a room."""
        with self.get_session() as session:
            statement = select(Message).where(
                Message.room == room
            ).order_by(Message.timestamp.desc()).limit(limit)
            return list(session.exec(statement).all())
    
    # Room operations
    def create_room(self, name: str, owner_id: int, 
                   description: Optional[str] = None) -> Room:
        """Create a new room."""
        with self.get_session() as session:
            room = Room(
                name=name,
                owner_id=owner_id,
                description=description
            )
            session.add(room)
            session.commit()
            session.refresh(room)
            return room
    
    def get_room(self, name: str) -> Optional[Room]:
        """Get room by name."""
        with self.get_session() as session:
            statement = select(Room).where(Room.name == name)
            return session.exec(statement).first()
    
    # File operations
    async def save_file(self, filename: str, content: bytes,
                       uploader_id: int, uploader_username: str,
                       room: str, mime_type: str) -> str:
        """Save uploaded file and return its path."""
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = Path(filename).name
        unique_filename = f"{timestamp}_{safe_filename}"
        file_path = Path(self.config.upload_dir) / unique_filename
        
        # Write file asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Save file metadata to database
        with self.get_session() as session:
            file_record = File(
                filename=unique_filename,
                original_filename=safe_filename,
                file_path=str(file_path),
                file_size=len(content),
                mime_type=mime_type,
                uploader_id=uploader_id,
                uploader_username=uploader_username,
                room=room
            )
            session.add(file_record)
            session.commit()
        
        return str(file_path)

