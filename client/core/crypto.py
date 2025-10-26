"""Cryptography module for local key management and encryption."""

import os
from pathlib import Path
from typing import Optional, Tuple
from nacl.public import PrivateKey, PublicKey, Box
from nacl.utils import random
from client.utils.logger import get_logger


logger = get_logger(__name__)


class CryptoManager:
    """Manages encryption keys and E2EE operations."""
    
    def __init__(self, key_dir: str = "keys"):
        """
        Initialize crypto manager.
        
        Args:
            key_dir: Directory to store keys
        """
        self.key_dir = Path(key_dir)
        self.key_dir.mkdir(exist_ok=True)
        
        self.private_key: Optional[PrivateKey] = None
        self.public_key: Optional[PublicKey] = None
        self.keypair_loaded = False
    
    def load_or_generate_keypair(self, username: str):
        """
        Load existing keypair or generate new one.
        
        Args:
            username: Username for key file naming
        """
        private_key_file = self.key_dir / f"{username}_private.key"
        public_key_file = self.key_dir / f"{username}_public.key"
        
        # Try to load existing keys
        if private_key_file.exists() and public_key_file.exists():
            try:
                self.private_key = PrivateKey(private_key_file.read_bytes())
                self.public_key = self.private_key.public_key
                self.keypair_loaded = True
                logger.info(f"Loaded keypair for {username}")
                return
            except Exception as e:
                logger.error(f"Error loading keys: {e}")
        
        # Generate new keypair
        logger.info(f"Generating new keypair for {username}")
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.keypair_loaded = True
        
        # Save keys
        private_key_file.write_bytes(bytes(self.private_key))
        public_key_file.write_bytes(bytes(self.public_key))
        
        logger.info(f"Keypair generated and saved for {username}")
    
    def get_public_key_encoded(self) -> str:
        """Get public key as base64 encoded string."""
        if not self.public_key:
            return ""
        import base64
        return base64.b64encode(bytes(self.public_key)).decode('utf-8')
    
    def encrypt_message(self, message: str, recipient_public_key: bytes) -> bytes:
        """
        Encrypt a message for a recipient.
        
        Args:
            message: Plain text message
            recipient_public_key: Recipient's public key bytes
            
        Returns:
            Encrypted message bytes
        """
        if not self.private_key:
            raise ValueError("No keypair loaded")
        
        try:
            recipient_pub = PublicKey(recipient_public_key)
            box = Box(self.private_key, recipient_pub)
            
            # Encrypt message
            encrypted = box.encrypt(message.encode('utf-8'))
            return encrypted
        
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_message(self, encrypted_message: bytes) -> str:
        """
        Decrypt a message using our private key.
        
        Args:
            encrypted_message: Encrypted message bytes
            
        Returns:
            Decrypted message string
        """
        if not self.private_key:
            raise ValueError("No keypair loaded")
        
        try:
            # Note: This assumes the message was encrypted with sender's private key
            # In production, use proper key exchange
            # For now, this is a stub implementation
            logger.warning("Decryption is simplified stub")
            return encrypted_message.decode('utf-8', errors='ignore')
        
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return ""
    
    def has_keypair(self) -> bool:
        """Check if keypair is loaded."""
        return self.keypair_loaded

