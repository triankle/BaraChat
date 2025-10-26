# BaraChat Quick Start Guide

## 🚀 Getting Started

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install aiohttp sqlmodel pyjwt pynacl PySide6 aiortc websockets Pillow pycryptodome bcrypt
```

### Step 2: Start the Server

Open a terminal and run:

```bash
cd server
python main.py
```

You should see:
```
LocalCord Server Active ✅
Server running at http://127.0.0.1:8765/
```

The server is now running and listening on port 8765.

### Step 3: Start the Client

Open **another terminal** and run:

```bash
cd client
python main.py
```

A PySide6 window will open with the BaraChat GUI.

### Step 4: Connect to Chat

1. In the client window, click on the **Settings** tab
2. Enter your username (e.g., "Alice")
3. Verify the server URL is `http://127.0.0.1:8765`
4. Click **Connect**

### Step 5: Send Messages

1. Click on a room in the left panel (e.g., "general")
2. Type a message in the input box at the bottom
3. Press **Enter** or click **Send**

Your messages will appear in the chat area with timestamps!

## 📖 Basic Usage

### Running Tests

```bash
pytest tests/
```

### Using the Development Script

```bash
# Start server
bash scripts/run_dev.sh server

# Start client
bash scripts/run_dev.sh client

# Run tests
bash scripts/run_dev.sh test
```

### Server Options

The server can be configured via environment variables:

```bash
# Windows PowerShell
$env:BARA_HOST="127.0.0.1"
$env:BARA_PORT="8765"
$env:BARA_DEBUG="true"
python server/main.py

# Linux/Mac
export BARA_HOST="127.0.0.1"
export BARA_PORT="8765"
export BARA_DEBUG="true"
python server/main.py
```

## 🎯 Current Features

✅ **Working:**
- Real-time text chat via WebSocket
- Multiple rooms/channels
- Multiple users in the same room
- Message broadcasting
- Server listening at http://127.0.0.1:8765

🔶 **To Be Implemented:**
- File upload/download
- User authentication (login/register)
- Voice chat
- End-to-end encryption

## ⚠️ Troubleshooting

**Issue:** `ModuleNotFoundError`
- **Solution:** Install all dependencies: `pip install -r requirements.txt`

**Issue:** Port already in use
- **Solution:** Change the port in `server/main.py` or set `BARA_PORT` env var

**Issue:** Client can't connect to server
- **Solution:** Make sure server is running first, check the URL in settings

**Issue:** Import errors
- **Solution:** Make sure you're running from the project root directory

## 📝 Development Tips

1. **Server logs** are displayed in the terminal
2. **Multiple clients** can connect to the same server
3. **Different rooms** for different chat channels
4. Check the server terminal for connection messages

## 🎮 Try It Now!

Open **three terminal windows**:

1. **Terminal 1** (Server):
   ```bash
   cd server && python main.py
   ```

2. **Terminal 2** (Client - Alice):
   ```bash
   cd client && python main.py
   ```

3. **Terminal 3** (Client - Bob):
   ```bash
   cd client && python main.py
   ```

Connect both clients to the same room and chat!

