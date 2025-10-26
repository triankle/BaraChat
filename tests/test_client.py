"""Tests for client functionality."""

import pytest
from client.core.network import NetworkClient
from client.core.crypto import CryptoManager


@pytest.fixture
def network_client():
    """Create a test network client."""
    return NetworkClient("http://127.0.0.1:8765")


@pytest.fixture
def crypto_manager():
    """Create a test crypto manager."""
    return CryptoManager()


def test_crypto_keypair(crypto_manager):
    """Test keypair generation."""
    crypto_manager.load_or_generate_keypair("testuser")
    
    assert crypto_manager.has_keypair()
    assert crypto_manager.private_key is not None
    assert crypto_manager.public_key is not None


def test_get_public_key_encoded(crypto_manager):
    """Test getting encoded public key."""
    crypto_manager.load_or_generate_keypair("testuser")
    
    key_str = crypto_manager.get_public_key_encoded()
    assert key_str is not None
    assert isinstance(key_str, str)
    assert len(key_str) > 0


def test_network_client_initialization(network_client):
    """Test network client initialization."""
    assert network_client.base_url == "http://127.0.0.1:8765"
    assert network_client.session is None
    assert network_client.websocket is None


def test_auth_token(network_client):
    """Test auth token management."""
    network_client.set_auth_token("test_token_123")
    headers = network_client.get_headers()
    
    assert 'Authorization' in headers
    assert headers['Authorization'] == 'Bearer test_token_123'

