"""Main application window."""

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QSplitter, QListWidget, QTabWidget
from PySide6.QtCore import Qt, Signal, QThread, QTimer, QObject
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
        self.setParent(None)  # Detach from QObject tree for easier cleanup
    
    def run(self):
        """Run asyncio event loop."""
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        except Exception as e:
            logger.error(f"AsyncWorker error: {e}")
        finally:
            if self.loop:
                try:
                    self.loop.close()
                except:
                    pass
    
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
        
        # Setup async worker
        self.async_worker = AsyncWorker()
        self.async_worker.start()
        
        # Connect signal
        self.message_received.connect(self._handle_message_received)
        
        self.setWindowTitle("BaraChat - Local Chat")
        self.setGeometry(100, 100, 1000, 700)
        
        self._setup_ui()
        
        logger.info("App window initialized")
    
    def _setup_ui(self):
        """Set up the UI layout."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel: Room list
        self.room_list = QListWidget()
        self.room_list.addItems(["general", "room-1", "room-2"])
        self.room_list.currentItemChanged.connect(self._on_room_changed)
        
        # Right panel: Chat area
        self.chat_tabs = QTabWidget()
        
        # Create a simple chat view for now
        from client.gui.chat_view import ChatView
        self.chat_view = ChatView()
        self.chat_tabs.addTab(self.chat_view, "Chat")
        
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
        """Handle room selection change."""
        if current:
            self.current_room = current.text()
            logger.info(f"Switched to room: {self.current_room}")
            # Update chat view for new room
            self.chat_view.clear()
    
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
    
    def _on_websocket_connected(self, connected):
        """Callback when WebSocket connection is established."""
        logger.info(f"WebSocket connected: {connected}")
        if connected:
            QTimer.singleShot(0, lambda: self.chat_view.add_message("System", "Connected to server!", 0))
    
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
    
    async def _on_message_received(self, data: dict):
        """Handle incoming message from WebSocket (runs in async context)."""
        user = data.get('user', 'unknown')
        text = data.get('text', '')
        timestamp = data.get('timestamp', 0)
        
        logger.info(f"Received message from {user}: {text[:50]}")
        
        # Only show if it's not from the current user (to avoid duplicates)
        # since we already show it immediately when sending
        if user != self.username:
            # Emit signal to update UI on main thread
            self.message_received.emit(user, text, timestamp)
    
    def send_message(self, text: str):
        """Send a message."""
        if self.network_client and self.username and text:
            # Show message immediately in the UI
            self.chat_view.add_message(self.username, text, 0)
            
            # Schedule async send to server
            self.async_worker.schedule_coroutine(
                self._send_message_async(text)
            )
            logger.info(f"Sent message: {text[:50]}")
    
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
    
    def closeEvent(self, event):
        """Clean up when window closes."""
        if self.async_worker:
            try:
                if self.async_worker.loop:
                    # Schedule cleanup tasks
                    self.async_worker.loop.call_soon_threadsafe(
                        self.async_worker.loop.stop
                    )
            except:
                pass
            self.async_worker.wait(2000)  # Wait up to 2 seconds
        super().closeEvent(event)

