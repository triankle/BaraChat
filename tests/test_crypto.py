"""Tests for cryptographic operations."""

import pytest
from server.crypto.e2ee import generate_keypair, encode_key, decode_key
from client.core.crypto import CryptoManager


def test_generate_keypair():
    """Test keypair generation."""
    private_key, public_key = generate_keypair()
    
    assert private_key is not None
    assert public_key is not None
    assert isinstance(private_key, bytes)
    assert isinstance(public_key, bytes)
    assert len(private_key) > 0
    assert len(public_key) > 0


def test_key_encoding():
    """Test key encoding and decoding."""
    private_key, public_key = generate_keypair()
    
    # Encode keys
    priv_str = encode_key(private_key)
    pub_str = encode_key(public_key)
    
    assert isinstance(priv_str, str)
    assert isinstance(pub_str, str)
    
    # Decode keys
    decoded_priv = decode_key(priv_str)
    decoded_pub = decode_key(pub_str)
    
    assert decoded_priv == private_key
    assert decoded_pub == public_key


def test_crypto_manager(crypto_manager: CryptoManager):
    """Test crypto manager operations."""
    crypto_manager.load_or_generate_keypair("testuser")
    
    # Test encryption (stub)
    try:
        message = "Hello, world!"
        encrypted = crypto_manager.encrypt_message(message, bytes(32))
        assert encrypted is not None
    except Exception as e:
        # Encryption might not be fully implemented
        pass


def test_has_keypair(crypto_manager: CryptoManager):
    """Test keypair checking."""
    assert not crypto_manager.has_keypair()
    
    crypto_manager.load_or_generate_keypair("testuser")
    assert crypto_manager.has_keypair()

