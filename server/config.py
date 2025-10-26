"""Server configuration management."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str = "127.0.0.1"
    port: int = 8765
    debug: bool = False
    
    # Database
    db_path: str = "barachat.db"
    upload_dir: str = "uploads"
    
    # SSL/TLS (for future HTTPS support)
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    
    # Security
    jwt_secret: str = "change-me-in-production"
    max_file_size: int = 50 * 1024 * 1024  # 50 MB
    
    # WebSocket
    ws_timeout: int = 30  # seconds


# Global configuration instance
_config: Optional[ServerConfig] = None


def load_config() -> ServerConfig:
    """Load configuration from environment variables or defaults."""
    global _config
    
    if _config is None:
        _config = ServerConfig(
            host=os.getenv("BARA_HOST", "127.0.0.1"),
            port=int(os.getenv("BARA_PORT", "8765")),
            debug=os.getenv("BARA_DEBUG", "false").lower() == "true",
            db_path=os.getenv("BARA_DB_PATH", "barachat.db"),
            upload_dir=os.getenv("BARA_UPLOAD_DIR", "uploads"),
            cert_file=os.getenv("BARA_CERT_FILE"),
            key_file=os.getenv("BARA_KEY_FILE"),
            jwt_secret=os.getenv("BARA_JWT_SECRET", "change-me-in-production"),
            max_file_size=int(os.getenv("BARA_MAX_FILE_SIZE", str(50 * 1024 * 1024))),
        )
        
        # Create upload directory if it doesn't exist
        Path(_config.upload_dir).mkdir(parents=True, exist_ok=True)
    
    return _config


def get_config() -> ServerConfig:
    """Get the current configuration."""
    if _config is None:
        return load_config()
    return _config

