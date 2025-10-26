# File Upload & Download Feature

## Overview
Added file upload and download functionality with clickable download links.

## Features

### ✅ Implemented:
- **📎 Attach File Button** - Click to select and upload files
- **File Download Links** - Clickable links to download files
- **Image Support** - Special handling for image files
- **File Storage** - Server stores files in memory
- **Auto-Display** - Files appear in chat with clickable links

## How to Use

### Upload a File:

1. **Click the 📎 button** next to the message input
2. **Select a file** from your computer
3. **File is uploaded** and a link appears in chat
4. **Other users see** the file link and can click to download

### Download a File:

1. **See file link** in chat (📎 filename)
2. **Click the link** to download
3. **File downloads** to your computer

### Files Supported:
- All files: `*.*`
- Images: `*.png, *.jpg, *.jpeg, *.gif, *.bmp`
- Documents: `*.pdf, *.doc, *.docx, *.txt`

## UI Elements

### Upload Button:
```
[📎]  - Click to attach file
```

### In Chat:
```
Alice (10:30:15)
📎 photo.png
🔗 Download File
```

## Implementation

### Client Side:
- **File Dialog**: Non-native dialog to avoid Windows issues
- **File Reading**: Reads file as binary
- **Upload**: Sends to server via multipart/form-data
- **Display**: Shows file link in chat

### Server Side:
- **Storage**: In-memory file storage dictionary
- **Upload Endpoint**: `/api/upload` - receives files
- **Download Endpoint**: `/download/{filename}` - serves files
- **Broadcast**: Sends file info to all users in room

## Files Modified

1. **client/gui/chat_view.py**:
   - Added 📎 attach button
   - Added file dialog with non-native option
   - Added file message display
   - Added clickable download links

2. **client/gui/app_window.py**:
   - Added `send_file()` method
   - Added `_send_file_async()` method
   - Updated message handling for files

3. **client/core/network.py**:
   - Updated `upload_file()` to accept file bytes
   - Changed from file path to file data

4. **server/main.py**:
   - Added file upload handler
   - Added file download handler
   - Added file storage dictionary

## Features

✅ **File Upload** - Click 📎 to attach files
✅ **File Download** - Click links to download
✅ **Image Detection** - Automatic image handling
✅ **Error Handling** - Graceful failure messages
✅ **Windows Compatible** - Uses non-native dialog

## Usage Example

1. **User A uploads file:**
   - Clicks 📎
   - Selects `photo.jpg`
   - Uploads successfully
   - File link appears in chat

2. **User B sees file:**
   - Sees "📎 photo.jpg 🔗 Download File"
   - Clicks download link
   - File downloads automatically

## Future Enhancements

- Image preview in chat (inline images)
- File size limits
- Progress indicators
- Multiple file upload
- Drag and drop files
- File type icons
- Preview before sending

## Status

✅ **Implemented:** File upload/download
✅ **Implemented:** Clickable download links
✅ **Implemented:** File type detection
✅ **Fixed:** Windows dialog error

You can now upload and share files in the chat!

