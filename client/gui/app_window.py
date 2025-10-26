"""Main application window."""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QSplitter, QListWidget, QTabWidget, QListWidgetItem
from PySide6.QtCore import Qt, Signal, QThread, QTimer, QObject
from PySide6.QtGui import QFont
from typing import Optional
from client.core.network import NetworkClient
from client.utils.logger import get_logger
import asyncio
import threading
from functools import partial


logger = get_logger(__name__)


class AsyncWorker(QThread):
    """Worker thread for async operations."""
    
    def __init__(self):
        super().__init__()
        self.loop = None
        self.is_terminating = False
    
    def run(self):
        """Run asyncio event loop."""
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        except Exception as e:
            if not self.is_terminating:
                logger.error(f"AsyncWorker error: {e}")
        finally:
            if self.loop:
                try:
                    # Cancel pending tasks
                    pending = asyncio.all_tasks(self.loop)
                    for task in pending:
                        task.cancel()
                    # Let tasks finish cancellation
                    self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    self.loop.close()
                except:
                    pass
    
    def request_stop(self):
        """Request the worker to stop."""
        self.is_terminating = True
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
    
    def schedule_coroutine(self, coro, callback=None):
        """Schedule a coroutine and optionally call callback when done."""
        future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        if callback:
            def check_result(fut):
                if fut.done():
                    try:
                        result = fut.result()
                        callback(result)
                    except Exception as e:
                        logger.error(f"Async operation failed: {e}")
            future.add_done_callback(check_result)
        return future


class AppWindow(QMainWindow):
    """Main application window."""
    
    # Signal for adding messages from async context
    message_received = Signal(str, str, float)
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.network_client: Optional[NetworkClient] = None
        self.current_room = "general"
        self.username = ""
        
        # Store conversation history per room
        self.room_histories = {}  # {room_name: [messages]}
        
        # Store channel data (text only for now)
        self.voice_channels = {
            "general": ["General Text"],
            "room-1": ["General Text"],
            "room-2": ["General Text"]
        }
        self.current_voice_channel = None  # Currently joined voice channel
        
        # Setup async worker
        self.async_worker = AsyncWorker()
        self.async_worker.start()
        
        # Connect signal
        self.message_received.connect(self._handle_message_received)
        
        self.setWindowTitle("BaraChat - Local Chat")
        self.setGeometry(100, 100, 1000, 700)
        
        self._setup_ui()
        
        logger.info("App window initialized")
    
    def _setup_channels(self):
        """Setup the room and channel list."""
        for room_name, channels in self.voice_channels.items():
            # Add room header
            room_item = QListWidgetItem(f"📢 {room_name.upper()}")
            room_item.setFlags(Qt.NoItemFlags)  # Not selectable
            room_item.setForeground(Qt.gray)
            font = QFont()
            font.setPointSize(10)
            font.setBold(True)
            room_item.setFont(font)
            self.room_list.addItem(room_item)
            
            # Add channels
            for channel in channels:
                item = QListWidgetItem(f"💬 {channel}")
                item.setData(Qt.UserRole, (room_name, channel))
                self.room_list.addItem(item)
    
    def _setup_ui(self):
        """Set up the UI layout."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel: Room and channel list
        self.room_list = QListWidget()
        self.room_list.currentItemChanged.connect(self._on_room_changed)
        
        # Add rooms and their channels
        self._setup_channels()
        
        # Right panel: Chat area
        self.chat_tabs = QTabWidget()
        
        # Create a simple chat view for now
        from client.gui.chat_view import ChatView
        self.chat_view = ChatView()
        self.chat_tabs.addTab(self.chat_view, "Chat")
        
        # Remove voice panel - not needed for now
        
        # Create settings view
        from client.gui.settings_view import SettingsView
        self.settings_view = SettingsView()
        self.settings_view.on_login.connect(self._on_login)
        self.chat_tabs.addTab(self.settings_view, "Settings")
        
        # Splitter layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.room_list)
        splitter.addWidget(self.chat_tabs)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(splitter)
    
    def _on_room_changed(self, current, previous):
        """Handle room/channel selection change."""
        if current:
            # Get room and channel info from item data
            item_data = current.data(Qt.UserRole)
            
            if item_data:  # This is a channel
                room_name, channel_name = item_data
                
                # Join text channel
                self._join_text_channel(room_name, channel_name)
            else:
                # Room header selected, do nothing
                pass
    
    def _join_text_channel(self, room_name: str, channel_name: str):
        """Join a text channel."""
        channel_id = f"{room_name}/{channel_name}"
        
        # Save current channel's history
        if self.current_room:
            self.room_histories[self.current_room] = self.chat_view.messages.copy()
        
        # Switch to new channel
        self.current_room = channel_id
        logger.info(f"Joined text channel: {channel_id}")
        
        # Load channel history
        self._load_room_history(channel_id)
        
        # Switch to chat tab
        self.chat_tabs.setCurrentIndex(0)
    
    def _join_voice_channel(self, room_name: str, channel_name: str):
        """Join a voice channel."""
        # Leave previous voice channel if joined
        if self.current_voice_channel:
            self._leave_voice_channel()
        
        # Join new voice channel
        self.current_voice_channel = f"{room_name}/{channel_name}"
        logger.info(f"Joined voice channel: {self.current_voice_channel}")
        
        # Voice panel removed - just show system message
        
        # Switch to voice tab
        self.chat_tabs.setCurrentIndex(1)
        
        # Show system message in chat
        self.chat_view.add_message("System", f"Joined voice channel: {channel_name}")
    
    def _leave_voice_channel(self):
        """Leave the current voice channel."""
        if self.current_voice_channel:
            logger.info(f"Left voice channel: {self.current_voice_channel}")
            self.current_voice_channel = None
    
    def _on_login(self, username: str, server_url: str):
        """
        Handle login from settings view.
        
        Args:
            username: Username
            server_url: Server URL
        """
        self.username = username
        logger.info(f"Login attempted: {username} @ {server_url}")
        
        # Initialize network client
        self.network_client = NetworkClient(server_url)
        
        # Connect to WebSocket asynchronously
        self.async_worker.schedule_coroutine(
            self._connect_websocket(),
            callback=self._on_websocket_connected
        )
        
        # Update UI
        self.chat_view.set_username(username)
    
    def _load_room_history(self, room: str):
        """Load conversation history for a room."""
        # Clear current view
        self.chat_view.clear()
        
        # Load history if it exists
        if room in self.room_histories:
            messages = self.room_histories[room]
            for msg in messages:
                if msg.get('type') == 'file':
                    # Handle file messages
                    self.chat_view.add_file_message(
                        msg['user'],
                        msg['filename'],
                        msg['file_url'],
                        msg.get('is_image', False),
                        msg['timestamp']
                    )
                else:
                    # Handle text messages
                    self.chat_view.add_message(
                        msg['user'],
                        msg['text'],
                        msg['timestamp']
                    )
            logger.info(f"Loaded history for room '{room}' ({len(messages)} messages)")
        else:
            # Initialize empty history for new room
            self.room_histories[room] = []
            logger.info(f"Created new history for room '{room}'")
    
    def _on_websocket_connected(self, connected):
        """Callback when WebSocket connection is established."""
        logger.info(f"WebSocket connected: {connected}")
        if connected:
            # Add system message to chat and history
            self.chat_view.add_message("System", "Connected to server!", 0)
            self.room_histories.setdefault(self.current_room, []).append({
                'user': "System",
                'text': "Connected to server!",
                'timestamp': 0
            })
    
    async def _connect_websocket(self):
        """Connect to WebSocket in background."""
        if self.network_client:
            try:
                await self.network_client.connect()
                connected = await self.network_client.connect_websocket(
                    self.current_room,
                    on_message=self._on_message_received
                )
                logger.info(f"WebSocket connection result: {connected}")
                return connected
            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")
                return False
    
    def _handle_message_received(self, user: str, text: str, timestamp: float):
        """Handle incoming message from signal (runs on main thread)."""
        self.chat_view.add_message(user, text, timestamp)
        
        # Update room history
        self.room_histories.setdefault(self.current_room, []).append({
            'user': user,
            'text': text,
            'timestamp': timestamp
        })
    
    async def _on_message_received(self, data: dict):
        """Handle incoming message from WebSocket (runs in async context)."""
        user = data.get('user', 'unknown')
        text = data.get('text', '')
        msg_type = data.get('type', 'text')
        timestamp = data.get('timestamp', 0)
        
        logger.info(f"Received message from {user}: {text[:50]}")
        
        # Only show if it's not from the current user (to avoid duplicates)
        # since we already show it immediately when sending
        if user == self.username:
            return
        
        if msg_type == 'file':
            # Handle file message
            # Parse filename and URL from text
            if '[FILE]' in text and ' - ' in text:
                parts = text.split(' - ', 1)
                filename = parts[0].replace('[FILE] ', '')
                file_url = parts[1] if len(parts) > 1 else f"/download/{filename}"
            else:
                filename = 'file'
                file_url = text
            
            is_image = filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
            
            # Emit special signal for file
            QTimer.singleShot(0, lambda: self.chat_view.add_file_message(
                user, filename, file_url, is_image, timestamp
            ))
            
            # Add to room history
            self.room_histories.setdefault(self.current_room, []).append({
                'user': user,
                'type': 'file',
                'filename': filename,
                'file_url': file_url,
                'is_image': is_image,
                'timestamp': timestamp
            })
        else:
            # Regular text message
            self.message_received.emit(user, text, timestamp)
    
    def send_message(self, text: str):
        """Send a message."""
        if self.network_client and self.username and text:
            # Show message immediately in the UI
            self.chat_view.add_message(self.username, text, 0)
            
            # Update room history
            self.room_histories.setdefault(self.current_room, []).append({
                'user': self.username,
                'text': text,
                'timestamp': 0
            })
            
            # Schedule async send to server
            self.async_worker.schedule_coroutine(
                self._send_message_async(text)
            )
            logger.info(f"Sent message to room '{self.current_room}': {text[:50]}")
    
    def send_file(self, filename: str, file_data: bytes, is_image: bool):
        """Send a file to the current room."""
        if self.network_client and self.username:
            # Show file in chat immediately
            # Use absolute URL for clickable links
            file_url = f"http://127.0.0.1:8765/download/{filename}"
            self.chat_view.add_file_message(self.username, filename, file_url, is_image, 0)
            
            # Update room history
            self.room_histories.setdefault(self.current_room, []).append({
                'user': self.username,
                'type': 'file',
                'filename': filename,
                'file_url': file_url,
                'is_image': is_image,
                'timestamp': 0
            })
            
            # Schedule async send
            self.async_worker.schedule_coroutine(
                self._send_file_async(filename, file_data, is_image)
            )
            logger.info(f"Sending file: {filename}")
    
    async def _send_file_async(self, filename: str, file_data: bytes, is_image: bool):
        """Upload and share a file."""
        if self.network_client:
            try:
                # Upload file to server
                result = await self.network_client.upload_file(
                    file_data=file_data,
                    filename=filename,
                    room=self.current_room
                )
                
                if result:
                    file_url = result.get('file_url', f'/download/{filename}')
                    # Make URL absolute for browser to open
                    absolute_url = f"http://127.0.0.1:8765{file_url}"
                    # Send as message
                    await self.network_client.send_message(
                        self.current_room,
                        self.username,
                        f"[FILE] {filename} - {absolute_url}",
                        msg_type="file"
                    )
                    logger.info(f"File uploaded: {filename}")
            except Exception as e:
                logger.error(f"Error uploading file: {e}")
    
    async def _send_message_async(self, text: str):
        """Send message async."""
        if self.network_client:
            try:
                result = await self.network_client.send_message(
                    self.current_room,
                    self.username,
                    text
                )
                return result
            except Exception as e:
                logger.error(f"Error sending message: {e}")
                return False
    
    
    def download_file(self, file_url: str):
        """Download a file from the given URL."""
        if self.network_client:
            # Schedule async download
            self.async_worker.schedule_coroutine(
                self._download_file_async(file_url)
            )
            logger.info(f"Downloading file from: {file_url}")
    
    async def _download_file_async(self, file_url: str):
        """Download file asynchronously."""
        import urllib.request
        from pathlib import Path
        from urllib.parse import unquote, quote
        
        try:
            # URL encode the filename properly
            # Split base URL and filename
            if '/download/' in file_url:
                base_url = file_url.split('/download/')[0]
                filename = file_url.split('/download/')[1]
                # Properly encode the filename
                encoded_filename = quote(filename, safe='')
                full_url = f"{base_url}/download/{encoded_filename}"
            else:
                full_url = file_url
                filename = file_url.split('/')[-1]
            
            # Decode filename for local storage
            local_filename = unquote(filename)
            
            downloads_dir = Path.home() / "Downloads"
            downloads_dir.mkdir(exist_ok=True)
            
            file_path = downloads_dir / local_filename
            
            # Download file using properly encoded URL
            logger.info(f"Downloading from: {full_url}")
            urllib.request.urlretrieve(full_url, str(file_path))
            
            self.chat_view.add_message(
                "System",
                f"✅ File downloaded to: {file_path}",
                0
            )
            logger.info(f"File downloaded to: {file_path}")
        
        except Exception as e:
            self.chat_view.add_message(
                "System",
                f"❌ Download failed: {e}",
                0
            )
            logger.error(f"Error downloading file: {e}")
    
    def closeEvent(self, event):
        """Clean up when window closes."""
        logger.info("Closing application...")
        
        # Disconnect network client if connected
        if self.network_client:
            try:
                # Schedule disconnect
                self.async_worker.schedule_coroutine(
                    self.network_client.disconnect()
                )
            except:
                pass
        
        # Stop async worker
        if self.async_worker:
            try:
                # Request stop
                self.async_worker.request_stop()
                
                # Wait for thread to finish gracefully
                if self.async_worker.isRunning():
                    self.async_worker.wait(1000)
            except Exception as e:
                logger.error(f"Error stopping async worker: {e}")
                # Force terminate if still running
                if self.async_worker.isRunning():
                    self.async_worker.terminate()
                    self.async_worker.wait(500)
        
        logger.info("Application closed")
        super().closeEvent(event)

