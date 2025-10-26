# BaraChat

A local, privacy-focused chat application - a self-hosted alternative to Discord.

## Features

- **Text Chat**: Real-time messaging with WebSocket
- **Voice Chat**: WebRTC-based voice communication (coming soon)
- **End-to-End Encryption**: Secure messaging with PyNaCl
- **File Sharing**: Upload and share files locally
- **Private & Secure**: Everything runs on your local network

## Architecture

```
BaraChat/
├── server/         # Local server (aiohttp, WebSocket)
├── client/         # Desktop app (PySide6 GUI)
├── common/         # Shared protocols and constants
├── tests/          # Unit and integration tests
├── scripts/        # Development utilities
└── packaging/      # Distribution packaging
```

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Quick Start

### Server Setup

```bash
cd server
python main.py
```

The server will start on `http://127.0.0.1:8765`

### Client Setup

```bash
cd client
python main.py
```

## Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
pytest tests/
```

## License

MIT

