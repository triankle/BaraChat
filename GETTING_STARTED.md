# BaraChat - Getting Started

## ✅ Installation Complete

All dependencies have been installed successfully!

## 🚀 How to Run

### Method 1: From Project Root (Recommended)

Open **two terminal windows** in the project directory:

**Terminal 1 - Server:**
```bash
python server/main.py
```

**Terminal 2 - Client:**
```bash
python client/main.py
```

### Method 2: Using Individual Commands

**Start the server:**
```bash
cd server
python main.py
```

**Start the client (in another terminal):**
```bash
cd client  
python main.py
```

## 📱 Using the Application

1. **Wait for the client window to open** (PySide6 GUI)

2. **Go to the "Settings" tab:**
   - Enter a username (e.g., "Alice")
   - Keep server URL as `http://127.0.0.1:8765`
   - Click "Connect"

3. **Go to the "Chat" tab:**
   - Select a room from the left panel (e.g., "general")
   - Type a message in the input box
   - Press Enter or click "Send"

## 🎮 Testing with Multiple Users

Open **another terminal** and run:
```bash
python client/main.py
```

Use a different username and chat with yourself in the same room!

## 🎯 Current Features

✅ **Working:**
- Text chat via WebSocket
- Multiple rooms/channels
- Multiple simultaneous users
- Real-time message broadcasting
- Modern GUI interface

## 📝 Configuration

### Server Options

Set environment variables before starting server:
```bash
# Windows PowerShell
$env:BARA_PORT="8765"
$env:BARA_HOST="127.0.0.1"

# Linux/Mac
export BARA_PORT="8765"
export BARA_HOST="127.0.0.1"
```

### Client Options

Change server URL in Settings tab before connecting.

## ⚠️ Troubleshooting

**"ModuleNotFoundError"**: Make sure you're running from project root or have installed dependencies

**"Address already in use"**: Change port or stop other services using port 8765

**Window doesn't open**: Check terminal for error messages

**Can't send messages**: Make sure server is running first

## 📚 Documentation

- `QUICKSTART.md` - Quick start guide
- `PROJECT_STRUCTURE.md` - Complete project structure
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `README.md` - Project overview

## 🎉 You're Ready!

The application is running. Start chatting! 🚀

