# Voice Channels Feature

## Overview
BaraChat now supports Discord-style voice channels! Each room (server) has both text and voice channels that you can join and leave.

## Structure

### Channel Organization:
```
📢 GENERAL
  💬 General Text
  🔊 Voice Channel 1
  🔊 Voice Channel 2

📢 ROOM-1
  💬 General Text
  🔊 Voice Channel 1

📢 ROOM-2
  💬 General Text
  🔊 Voice Channel 1
```

## How It Works

### Channel Types:

1. **Text Channels (💬)**
   - For text messaging
   - Conversation history preserved
   - Shows in Chat tab

2. **Voice Channels (🔊)**
   - For voice chat
   - Join to enter voice chat
   - Switch to Voice tab automatically
   - Shows current voice channel status

### Navigation:

1. **Select a Channel:**
   - Click a channel in the left sidebar
   - Text channels → opens Chat tab
   - Voice channels → opens Voice tab and joins

2. **Voice Channel Features:**
   - Auto-joins when selected
   - Stays connected until you leave
   - Shows status in voice panel
   - Push-to-talk button for talking

## Usage

### Joining Voice Channels:

1. **Start the app:**
   ```bash
   python client/main.py
   ```

2. **Navigate channels:**
   - Click a voice channel (e.g., "🔊 Voice Channel 1")
   - Voice tab opens automatically
   - Status shows "🔊 In Voice: Voice Channel 1"

3. **Talk in voice:**
   - Hold "Press to Talk" button
   - Speak while holding
   - Release to stop

### Leaving Voice Channels:

**Method 1:** Switch to another channel
- Click any other channel
- Automatically leaves current voice channel

**Method 2:** Disconnect from Settings
- Mute yourself or close app

## Features

✅ **Persistent Voice Channels:** Stay in voice until you leave
✅ **Visual Indicators:** Status shows which voice channel you're in
✅ **Channel List:** See all available channels per room
✅ **Room Headers:** Organized by server/room
✅ **Text vs Voice:** Clear distinction between channel types
✅ **Auto-Switch:** Tab switches automatically based on channel type

## Channel Status

### Connected States:
- **Green "In Voice: ..."** - Active in voice channel
- **Gray "Not Connected"** - Not in any voice channel
- **Yellow "Muted"** - In voice but microphone muted

### Channel List Icons:
- 💬 - Text channel
- 🔊 - Voice channel
- 📢 - Room header (not selectable)

## Implementation

### Files Modified:
- `client/gui/app_window.py` - Channel system and voice joining logic
- Server already has voice signaling endpoint at `/voice`

### Channel Management:
```python
self.voice_channels = {
    "general": ["General Text", "Voice Channel 1", "Voice Channel 2"],
    "room-1": ["General Text", "Voice Channel 1"],
    "room-2": ["General Text", "Voice Channel 1"]
}
```

### Key Methods:
- `_join_text_channel()` - Switch to text chat
- `_join_voice_channel()` - Join voice and switch to Voice tab
- `_leave_voice_channel()` - Disconnect from voice
- `_setup_channels()` - Build the channel list UI

## Testing

1. **Start Application:**
   ```bash
   python client/main.py
   ```

2. **Test Text Channel:**
   - Click "💬 General Text"
   - Type a message
   - Send it

3. **Test Voice Channel:**
   - Click "🔊 Voice Channel 1"
   - Notice Voice tab opens
   - See status change to "In Voice"
   - Test push-to-talk

4. **Test Switching:**
   - Join voice channel
   - Switch to text channel
   - Switch back to voice
   - Status remains correct

## Status

✅ **Implemented:** Discord-style voice channels
✅ **Implemented:** Channel navigation
✅ **Implemented:** Voice channel persistence
✅ **Implemented:** Auto-tab switching
✅ **Implemented:** Visual status indicators

The voice channel system is now fully functional!

