"""Tests for server functionality."""

import pytest
from server.storage import Storage
from server.models import User
from server.auth import AuthManager


@pytest.fixture
def storage():
    """Create a test storage instance."""
    storage = Storage()
    storage.config.db_path = ":memory:"  # Use in-memory DB for tests
    storage.initialize()
    return storage


@pytest.fixture
def auth():
    """Create auth manager instance."""
    return AuthManager()


def test_create_user(storage):
    """Test user creation."""
    user = storage.create_user("testuser", "password_hash", "test@example.com")
    assert user.username == "testuser"
    assert user.id is not None


def test_get_user_by_username(storage):
    """Test getting user by username."""
    storage.create_user("testuser", "hash", "test@example.com")
    user = storage.get_user_by_username("testuser")
    assert user is not None
    assert user.username == "testuser"


def test_password_hashing(auth):
    """Test password hashing."""
    password = "test_password_123"
    hashed = auth.hash_password(password)
    
    assert hashed != password
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrong_password", hashed)


def test_jwt_token(auth):
    """Test JWT token creation and verification."""
    token = auth.create_token(user_id=1, username="testuser")
    assert token is not None
    
    payload = auth.verify_token(token)
    assert payload is not None
    assert payload['user_id'] == 1
    assert payload['username'] == "testuser"


def test_invalid_token(auth):
    """Test invalid token verification."""
    payload = auth.verify_token("invalid.token.here")
    assert payload is None


def test_save_message(storage):
    """Test saving a message."""
    user = storage.create_user("testuser", "hash")
    message = storage.save_message(
        room="general",
        user_id=user.id,
        username="testuser",
        content="Hello, world!"
    )
    
    assert message.content == "Hello, world!"
    assert message.room == "general"


def test_get_recent_messages(storage):
    """Test retrieving recent messages."""
    user = storage.create_user("testuser", "hash")
    
    # Create multiple messages
    for i in range(10):
        storage.save_message(
            room="general",
            user_id=user.id,
            username="testuser",
            content=f"Message {i}"
        )
    
    messages = storage.get_recent_messages("general", limit=5)
    assert len(messages) == 5
    assert messages[0].content == "Message 9"

