# Conversation History Per Room

## Problem
When switching between rooms (channels), the conversation history was being cleared. This meant that switching rooms would lose all messages that were sent.

## Root Cause
The original implementation called `self.chat_view.clear()` when switching rooms, which removed all messages from the display. There was no mechanism to save and restore conversation history.

## Solution

### 1. **Conversation History Storage**
Added a dictionary to store conversation history per room:
```python
self.room_histories = {}  # {room_name: [messages]}
```

### 2. **Save History on Room Switch**
When switching from one room to another, the current room's conversation is saved:
```python
def _on_room_changed(self, current, previous):
    if previous:
        old_room = previous.text()
        self.room_histories[old_room] = self.chat_view.messages.copy()
```

### 3. **Load History When Entering Room**
When entering a room, its conversation history is loaded:
```python
def _load_room_history(self, room: str):
    if room in self.room_histories:
        messages = self.room_histories[room]
        for msg in messages:
            self.chat_view.add_message(msg['user'], msg['text'], msg['timestamp'])
```

### 4. **Track Messages in History**
Every message sent or received is automatically added to the room's history:
```python
def send_message(self, text: str):
    self.chat_view.add_message(self.username, text, 0)
    # Save to history
    self.room_histories.setdefault(self.current_room, []).append({
        'user': self.username,
        'text': text,
        'timestamp': 0
    })
```

## How It Works

### Message Flow:

1. **Switching Rooms:**
   - User selects a different room in the list
   - Current room's messages are saved to `room_histories`
   - New room's history is loaded into the chat view
   - If it's a new room, an empty history is created

2. **Sending Messages:**
   - Message appears in chat immediately
   - Message is added to current room's history
   - Message is sent to server

3. **Receiving Messages:**
   - Message is received from WebSocket
   - Message appears in chat
   - Message is added to current room's history

### Benefits:

✅ **Persistent History:** Messages are preserved when switching rooms
✅ **Per-Room Storage:** Each room has its own conversation history
✅ **Automatic Tracking:** All messages are automatically saved
✅ **No Data Loss:** Switching rooms no longer clears conversations

## Testing

1. Start the application
2. Go to room "general"
3. Send a few messages
4. Switch to room "room-1"
5. Send a few messages there
6. Switch back to "general"
7. **All your messages should still be there!**

## Files Modified

- `client/gui/app_window.py` - Added room history storage and management

## Status

✅ **Fixed:** Conversation history is now preserved per room
✅ **Fixed:** Switching rooms no longer clears messages
✅ **Added:** Automatic history tracking for all messages

