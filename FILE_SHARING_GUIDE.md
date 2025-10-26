# File Sharing Feature

## Overview
BaraChat now supports file upload and download functionality! Users can share files in chat rooms.

## Features

### ✅ Upload Files
- Click 📎 button to attach files
- Select any file from your computer
- File is uploaded to server and shared in chat
- Clickable download links appear in messages

### ✅ Download Files
- Click download link in chat message
- File downloads to your Downloads folder
- Download button shows last available file
- Works with all file types

### ✅ Supported File Types
- **Images**: PNG, JPG, JPEG, GIF, BMP
- **Documents**: PDF, DOC, DOCX, TXT
- **All Files**: Any file type supported

## How to Use

### Upload a File:
1. Click the **📎** button in chat input
2. Select a file from your computer
3. File appears in chat with download link
4. All users in the room can download it

### Download a File:
1. See a file link in chat (📎 filename)
2. Click the **📥 Download** link
3. File downloads to your Downloads folder
4. Or use the Download button at bottom of chat

## Visual Indicators

### File Messages:
- **📎** For regular files
- **📷** For images  
- **📥 Download** - Clickable link

### Download Button:
- Shows at bottom of chat
- Displays last file available
- Green "📥 Download" button when file available
- Gray/disabled when no file

## Technical Implementation

### Upload Flow:
```
User clicks 📎 → Select file → Upload to server → 
Broadcast to room → All users see download link
```

### Download Flow:
```
User clicks link → Client downloads → Saves to Downloads folder → 
Shows "File downloaded" message
```

### Server Storage:
- Files stored in memory (UPLOADED_FILES dict)
- Files accessible via `/download/{filename}` endpoint
- URL encoding handles special characters in filenames

## Files Modified

### Client:
- `client/gui/chat_view.py` - Added file button and download UI
- `client/gui/app_window.py` - File upload/download handlers
- `client/core/network.py` - Upload API calls

### Server:
- `server/main.py` - File upload/download endpoints

## Architecture

### Upload Endpoint:
- **POST** `/api/upload`
- Accepts multipart/form-data
- Stores file in memory
- Returns file URL

### Download Endpoint:
- **GET** `/download/{filename}`
- Serves file content
- Supports URL-encoded filenames
- Proper MIME type handling

## Usage Tips

1. **File Size:** Large files may take time to upload
2. **Room Sharing:** Files are shared in the current room only
3. **Downloads:** Click link or use bottom button
4. **Multiple Files:** Each upload creates a new download link

## Status

✅ **Implemented:** File upload with GUI button
✅ **Implemented:** File download via links
✅ **Implemented:** Download button for last file
✅ **Implemented:** Image file detection
✅ **Implemented:** All file type support

File sharing is now fully functional!

