"""Voice chat panel with dynamic voice detection and mute controls."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal, QTimer
from client.utils.logger import get_logger


logger = get_logger(__name__)


class VoicePanel(QWidget):
    """Voice chat panel with dynamic voice transmission."""
    
    # Signals for voice events
    voice_toggled = Signal(bool)  # Emitted when voice state changes
    mute_toggled = Signal(bool)  # Emitted when mute state changes
    
    def __init__(self):
        """Initialize voice panel."""
        super().__init__()
        
        self.is_muted = False
        self.is_enabled = True  # Voice is always-on when enabled
        self.echo_test_active = False
        
        self._setup_ui()
        
        # Create timers
        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self._check_voice_activity)
        
        self.echo_timer = QTimer()
        self.echo_timer.timeout.connect(self._process_echo)
        self.echo_buffer = []
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Status indicator
        self.status_label = QLabel("Voice channel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Current room indicator
        self.room_label = QLabel("Connected to: general")
        self.room_label.setAlignment(Qt.AlignCenter)
        self.room_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.room_label)
        
        layout.addSpacing(20)
        
        # Mute button
        self.mute_button = QPushButton("🔊 Mute")
        self.mute_button.clicked.connect(self._toggle_mute)
        self.mute_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)
        layout.addWidget(self.mute_button)
        
        # Voice activation toggle
        self.voice_toggle = QPushButton("🎤 Voice ON")
        self.voice_toggle.setCheckable(True)
        self.voice_toggle.setChecked(True)
        self.voice_toggle.clicked.connect(self._toggle_voice)
        self.voice_toggle.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:checked {
                background-color: #28a745;
            }
            QPushButton:!checked {
                background-color: #6c757d;
            }
        """)
        layout.addWidget(self.voice_toggle)
        
        # Voice level indicator (simulated)
        self.level_indicator = QLabel("Voice level: ▯▯▯▯▯")
        self.level_indicator.setAlignment(Qt.AlignCenter)
        self.level_indicator.setStyleSheet("color: #888; font-size: 12px; margin-top: 5px;")
        layout.addWidget(self.level_indicator)
        
        # Test Voice toggle button
        self.test_voice_button = QPushButton("🎙️ Echo Test OFF")
        self.test_voice_button.setCheckable(True)
        self.test_voice_button.setChecked(False)
        self.test_voice_button.clicked.connect(self._toggle_echo_test)
        self.test_voice_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:checked {
                background-color: #17a2b8;
            }
        """)
        layout.addWidget(self.test_voice_button)
        
        # Test feedback label
        self.test_feedback = QLabel("")
        self.test_feedback.setAlignment(Qt.AlignCenter)
        self.test_feedback.setStyleSheet("color: #28a745; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.test_feedback)
        
        # Info label
        info_label = QLabel("Voice ON = Speak naturally | Echo Test = Hear your voice with 0.5s delay")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #888; font-size: 10px; margin-top: 10px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
    
    def set_room(self, room_name: str):
        """Update the current room indicator."""
        self.room_label.setText(f"Connected to: {room_name}")
        logger.info(f"Voice panel room set to: {room_name}")
    
    def _toggle_mute(self):
        """Toggle mute state."""
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.mute_button.setText("🔇 Unmute")
            self.mute_button.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            self.status_label.setText("Voice channel (Muted)")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #ffc107;
                    color: black;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
        else:
            self.mute_button.setText("🔊 Mute")
            self.mute_button.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
                QPushButton:pressed {
                    background-color: #004578;
                }
            """)
            self.status_label.setText("Voice channel")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #28a745;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
        
        self.mute_toggled.emit(self.is_muted)
        logger.info(f"Mute toggled: {self.is_muted}")
    
    def _toggle_voice(self):
        """Toggle voice transmission on/off."""
        self.is_enabled = not self.is_enabled
        if self.is_enabled:
            self.voice_toggle.setText("🎤 Voice ON")
            self.voice_toggle.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 20px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            self.status_label.setText("Voice channel (Active)")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #28a745;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            # Start voice activity simulation
            self.activity_timer.start(100)  # Check every 100ms
        else:
            self.voice_toggle.setText("🔇 Voice OFF")
            self.voice_toggle.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 20px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
            self.status_label.setText("Voice channel (Disabled)")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #6c757d;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
            """)
            # Stop voice activity simulation
            self.activity_timer.stop()
            self.level_indicator.setText("Voice level: ▯▯▯▯▯")
        
        self.voice_toggled.emit(self.is_enabled)
        logger.info(f"Voice toggled: {self.is_enabled}")
    
    def _check_voice_activity(self):
        """Simulate voice activity detection."""
        # In production, this would read from actual microphone input
        # For now, simulate random voice activity
        import random
        if random.random() > 0.7:  # 30% chance of activity
            self.level_indicator.setText("Voice level: ▮▮▮▮▮")
        else:
            self.level_indicator.setText("Voice level: ▮▮▯▯▯")
    
    def start_voice(self):
        """Start voice transmission."""
        if not self.is_muted and self.is_enabled:
            self.activity_timer.start(100)
    
    def stop_voice(self):
        """Stop voice transmission."""
        self.activity_timer.stop()
        self.level_indicator.setText("Voice level: ▯▯▯▯▯")
    
    def _toggle_echo_test(self):
        """Toggle echo test on/off."""
        self.echo_test_active = not self.echo_test_active
        
        if self.echo_test_active:
            self.test_voice_button.setText("🎙️ Echo Test ON")
            self.test_feedback.setText("🔊 Echo test active - You'll hear your voice with 0.5s delay")
            self.test_feedback.setStyleSheet("color: #17a2b8; font-size: 11px; font-weight: bold;")
            
            # Start echo processing
            self.echo_timer.start(20)  # Process every 20ms for ~50fps audio
            logger.info("Echo test started")
        else:
            self.test_voice_button.setText("🎙️ Echo Test OFF")
            self.test_feedback.setText("")
            self.echo_timer.stop()
            self.echo_buffer.clear()
            logger.info("Echo test stopped")
    
    def _process_echo(self):
        """Process echo feedback with 0.5 second delay."""
        # Simulate capturing audio
        import random
        
        # Simulate current voice level
        level = random.randint(0, 5)
        level_bars = "▮" * level + "▯" * (5 - level)
        self.level_indicator.setText(f"Voice level: {level_bars}")
        
        # Add to buffer (simulating 0.5s = 25 samples at 20ms intervals)
        self.echo_buffer.append(level)
        if len(self.echo_buffer) > 25:  # 25 * 20ms = 0.5 seconds
            delayed_level = self.echo_buffer.pop(0)
            
            # Play back the delayed audio (simulated)
            delayed_level_bars = "▮" * delayed_level + "▯" * (5 - delayed_level)
            
            # Show echo feedback
            if delayed_level >= 3:
                self.test_feedback.setText(f"🔊 Echo: {delayed_level_bars} (Hearing your voice!)")
                self.test_feedback.setStyleSheet("color: #28a745; font-size: 11px; font-weight: bold;")
            elif delayed_level >= 1:
                self.test_feedback.setText(f"🔊 Echo: {delayed_level_bars}")
                self.test_feedback.setStyleSheet("color: #17a2b8; font-size: 11px; font-weight: bold;")
            else:
                self.test_feedback.setText("🔇 Echo test active - Speak to hear feedback")
                self.test_feedback.setStyleSheet("color: #6c757d; font-size: 11px; font-weight: bold;")

