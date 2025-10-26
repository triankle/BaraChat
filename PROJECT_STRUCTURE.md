# BaraChat Project Structure

This document describes the complete project structure of BaraChat.

## 📁 Complete File Structure

```
BaraChat/
├── README.md                      # Project overview
├── pyproject.toml                 # Python project configuration
├── requirements.txt                # Python dependencies
├── .gitignore                     # Git ignore rules
├── PROJECT_STRUCTURE.md          # This file
│
├── server/                        # Local server (aiohttp + WebSocket)
│   ├── __init__.py
│   ├── main.py                    # ✅ Entry point (already implemented)
│   ├── config.py                  # ✅ Configuration management
│   ├── models.py                  # ✅ ORM models (SQLModel)
│   ├── storage.py                 # ✅ Database & file handling
│   ├── auth.py                    # ✅ JWT authentication
│   ├── api/
│   │   ├── __init__.py
│   │   ├── rest.py                # ✅ REST API endpoints
│   │   └── ws_text.py             # ✅ Text chat WebSocket
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── signaling.py           # 🔶 WebRTC signaling (stub)
│   │   └── sfu_stub.py            # 🔶 SFU stub (future)
│   ├── crypto/
│   │   ├── __init__.py
│   │   └── e2ee.py                # 🔶 E2EE helpers (stub)
│   └── utils/
│       ├── __init__.py
│       └── logger.py              # ✅ Logging configuration
│
├── client/                        # Desktop application (PySide6)
│   ├── __init__.py
│   ├── main.py                    # ✅ GUI entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── network.py             # ✅ REST + WebSocket client
│   │   ├── crypto.py              # ✅ Local key management
│   │   └── media.py               # 🔶 Voice chat (stub)
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app_window.py          # ✅ Main window
│   │   ├── chat_view.py           # ✅ Text chat view
│   │   ├── voice_panel.py         # 🔶 Voice chat (stub)
│   │   ├── settings_view.py       # ✅ Settings UI
│   │   └── qml/                   # QML UI (placeholder)
│   │       ├── main.qml
│   │       ├── components/
│   │       └── themes/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py               # ✅ Logging utilities
│   └── assets/
│       ├── icons/                 # App icons
│       └── images/                # App images
│
├── common/                        # Shared modules
│   ├── __init__.py
│   ├── protocol.py                # ✅ JSON message schemas
│   └── constants.py               # ✅ Shared constants
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_server.py             # ✅ Server tests
│   ├── test_client.py             # ✅ Client tests
│   └── test_crypto.py              # ✅ Crypto tests
│
├── scripts/                       # CLI utilities
│   ├── gen_selfsigned_cert.sh     # 🔶 SSL certificate generator
│   └── run_dev.sh                 # 🔶 Development helper
│
└── packaging/                     # Distribution
    ├── build.spec                 # PyInstaller config
    └── install_instructions.md    # Packaging guide

```

## 📊 Implementation Status

### ✅ Fully Implemented
- Server core (config, models, storage, auth)
- REST API endpoints (file upload/download)
- WebSocket text chat
- Client network layer
- Basic GUI (app window, chat view, settings)
- Common protocols and constants
- Test suite structure

### 🔶 Stub/Partial Implementation
- Voice chat (WebRTC signaling skeleton)
- E2EE encryption (PyNaCl stubs)
- QML UI files (placeholder)
- Certificate generation scripts

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
cd server
python main.py
```
Server runs on `http://127.0.0.1:8765`

### 3. Start the Client
```bash
cd client
python main.py
```

## 🧪 Running Tests
```bash
pytest tests/
```

## 📝 Notes

- All code is commented in English
- Uses async/await throughout
- Modular architecture for easy extension
- Follows PEP 8 style guidelines
- All modules include docstrings and type hints

