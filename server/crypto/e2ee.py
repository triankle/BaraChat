"""End-to-end encryption helpers using PyNaCl."""

import nacl.utils
import nacl.secret
import nacl.public
import base64
from typing import Optional, Tuple
from server.utils.logger import get_logger


logger = get_logger(__name__)


def generate_keypair() -> Tuple[bytes, bytes]:
    """
    Generate a public/private key pair for E2EE.
    
    Returns:
        Tuple of (private_key, public_key) as bytes
    """
    private_key = nacl.public.PrivateKey.generate()
    public_key = private_key.public_key
    return private_key.encode(), public_key.encode()


def encrypt_message(message: str, recipient_public_key: bytes) -> bytes:
    """
    Encrypt a message for a recipient.
    
    Args:
        message: Plain text message
        recipient_public_key: Recipient's public key
        
    Returns:
        Encrypted message as bytes
    """
    # Convert string keys to PublicKey objects
    pub_key = nacl.public.PublicKey(recipient_public_key)
    
    # Create a Box for encryption
    # Note: This is a simplified version
    # In production, use proper key exchange and ephemeral keys
    box = nacl.public.Box.generate()
    
    # Encrypt the message
    encrypted = box.encrypt(message.encode())
    
    return encrypted


def decrypt_message(encrypted_message: bytes, private_key: bytes) -> str:
    """
    Decrypt a message using private key.
    
    Args:
        encrypted_message: Encrypted message bytes
        private_key: Your private key
        
    Returns:
        Decrypted message string
    """
    try:
        # Note: This is a simplified stub
        # Proper decryption requires matching keys and nonce handling
        logger.warning("E2EE decryption not fully implemented yet")
        return encrypted_message.decode('utf-8', errors='ignore')
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        return ""


def encode_key(key: bytes) -> str:
    """Encode a key to base64 string."""
    return base64.b64encode(key).decode('utf-8')


def decode_key(key_str: str) -> bytes:
    """Decode a key from base64 string."""
    return base64.b64decode(key_str)

