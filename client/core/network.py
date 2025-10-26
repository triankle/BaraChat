"""Network layer for REST API and WebSocket client."""

import asyncio
import json
import aiohttp
import websockets
from typing import Optional, Callable, Dict, Any
from client.utils.logger import get_logger


logger = get_logger(__name__)


class NetworkClient:
    """Handles REST API calls and WebSocket connections."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8765"):
        """
        Initialize network client.
        
        Args:
            base_url: Server base URL
        """
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.message_callbacks: list[Callable] = []
        self.auth_token: Optional[str] = None
    
    async def connect(self):
        """Create HTTP session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def disconnect(self):
        """Close HTTP session and WebSocket."""
        try:
            if self.websocket:
                await self.websocket.close()
                self.websocket = None
        except Exception as e:
            logger.error(f"Error closing WebSocket: {e}")
        
        try:
            if self.session and not self.session.closed:
                await self.session.close()
                self.session = None
        except Exception as e:
            logger.error(f"Error closing session: {e}")
    
    def set_auth_token(self, token: str):
        """Set authentication token."""
        self.auth_token = token
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers with authentication if available."""
        headers = {}
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
        return headers
    
    async def register(self, username: str, password: str, email: Optional[str] = None) -> Dict[str, Any]:
        """
        Register a new user.
        
        Args:
            username: Username
            password: Password
            email: Email (optional)
            
        Returns:
            Response data
        """
        await self.connect()
        
        try:
            url = f"{self.base_url}/api/register"
            data = {
                'username': username,
                'password': password,
                'email': email
            }
            
            async with self.session.post(url, json=data) as response:
                return await response.json()
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            raise
    
    async def login(self, username: str, password: str) -> Optional[str]:
        """
        Login and get auth token.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Auth token or None if failed
        """
        await self.connect()
        
        try:
            url = f"{self.base_url}/api/login"
            data = {
                'username': username,
                'password': password
            }
            
            async with self.session.post(url, json=data) as response:
                result = await response.json()
                
                if 'token' in result:
                    self.auth_token = result['token']
                    return self.auth_token
                return None
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            return None
    
    async def upload_file(self, file_path: str, room: str) -> Dict[str, Any]:
        """
        Upload a file.
        
        Args:
            file_path: Path to file
            room: Target room name
            
        Returns:
            Upload response data
        """
        await self.connect()
        
        try:
            url = f"{self.base_url}/api/upload"
            
            with open(file_path, 'rb') as f:
                form_data = aiohttp.FormData()
                form_data.add_field('file', f, filename=file_path)
                form_data.add_field('room', room)
                
                headers = self.get_headers()
                
                async with self.session.post(url, data=form_data, headers=headers) as response:
                    return await response.json()
        
        except Exception as e:
            logger.error(f"File upload error: {e}")
            raise
    
    async def connect_websocket(self, room: str, 
                               on_message: Optional[Callable] = None) -> bool:
        """
        Connect to WebSocket for chat.
        
        Args:
            room: Room name
            on_message: Callback for incoming messages
            
        Returns:
            True if connected successfully
        """
        try:
            ws_url = self.base_url.replace('http', 'ws') + f"/ws?room={room}"
            
            self.websocket = await websockets.connect(ws_url)
            
            if on_message:
                self.message_callbacks.append(on_message)
            
            # Start listening for messages
            asyncio.create_task(self._listen_messages())
            
            logger.info(f"Connected to WebSocket in room '{room}'")
            return True
        
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            return False
    
    async def _listen_messages(self):
        """Listen for incoming WebSocket messages."""
        try:
            async for message in self.websocket:
                # Parse message
                try:
                    data = json.loads(message)
                    logger.info(f"Received WebSocket message: {data}")
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    continue
                
                # Notify callbacks
                for callback in self.message_callbacks:
                    try:
                        await callback(data)
                    except Exception as e:
                        logger.error(f"Message callback error: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket closed")
        except Exception as e:
            logger.error(f"Error listening for messages: {e}")
    
    async def send_message(self, room: str, user: str, text: str, 
                          msg_type: str = "text") -> bool:
        """
        Send a text message through WebSocket.
        
        Args:
            room: Room name
            user: Username
            text: Message text
            msg_type: Message type
            
        Returns:
            True if sent successfully
        """
        if not self.websocket:
            logger.warning("WebSocket not connected")
            return False
        
        try:
            message = {
                'type': msg_type,
                'room': room,
                'user': user,
                'text': text
            }
            
            await self.websocket.send(json.dumps(message))
            return True
        
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def on_message(self, callback: Callable):
        """Register a message callback."""
        self.message_callbacks.append(callback)

