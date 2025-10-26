"""Authentication and authorization."""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from server.config import get_config
from server.models import User


class AuthManager:
    """Handles authentication, JWT tokens, and password hashing."""
    
    def __init__(self):
        self.config = get_config()
        self.secret = self.config.jwt_secret
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a hash."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    def create_token(self, user_id: int, username: str, 
                    expires_in: int = 24 * 60 * 60) -> str:
        """
        Create a JWT token.
        
        Args:
            user_id: User ID
            username: Username
            expires_in: Token expiration in seconds (default 24 hours)
            
        Returns:
            JWT token string
        """
        now = datetime.utcnow()
        payload = {
            'user_id': user_id,
            'username': username,
            'iat': now,
            'exp': now + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def extract_token_from_header(self, auth_header: Optional[str]) -> Optional[str]:
        """
        Extract token from Authorization header.
        
        Args:
            auth_header: Authorization header value (e.g., "Bearer <token>")
            
        Returns:
            Token string or None
        """
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        return auth_header[7:]  # Remove "Bearer " prefix
    
    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user info from token if valid."""
        payload = self.verify_token(token)
        if payload:
            return {
                'user_id': payload.get('user_id'),
                'username': payload.get('username')
            }
        return None


# Global auth manager instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get the global auth manager instance."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager

