"""REST API endpoints for file uploads and user management."""

from aiohttp import web, MultipartReader
from pathlib import Path
from typing import Optional
from server.config import get_config
from server.storage import Storage
from server.auth import get_auth_manager
from server.utils.logger import get_logger


logger = get_logger(__name__)


async def handle_upload(request: web.Request) -> web.Response:
    """
    Handle file upload endpoint.
    
    Expected multipart/form-data with:
    - file: the file to upload
    - room: target room name
    - user: username
    
    Returns JSON with file URL and metadata.
    """
    config = get_config()
    storage = Storage()
    auth = get_auth_manager()
    
    try:
        # Check authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return web.json_response(
                {'error': 'Authentication required'},
                status=401
            )
        
        token = auth.extract_token_from_header(auth_header)
        user_info = auth.get_user_from_token(token)
        
        if not user_info:
            return web.json_response(
                {'error': 'Invalid token'},
                status=401
            )
        
        # Parse multipart data
        reader = await request.multipart()
        file_obj = None
        room = None
        
        async for part in reader:
            if part.name == 'file':
                file_obj = part
            elif part.name == 'room':
                room = await part.text()
        
        if not file_obj or not room:
            return web.json_response(
                {'error': 'Missing file or room'},
                status=400
            )
        
        # Read file content
        filename = file_obj.filename or 'unknown'
        content = await file_obj.read()
        
        # Check file size
        if len(content) > config.max_file_size:
            return web.json_response(
                {'error': f'File too large (max {config.max_file_size} bytes)'},
                status=413
            )
        
        # Check MIME type
        mime_type = file_obj.content_type or 'application/octet-stream'
        
        # Save file
        file_path = await storage.save_file(
            filename=filename,
            content=content,
            uploader_id=user_info['user_id'],
            uploader_username=user_info['username'],
            room=room,
            mime_type=mime_type
        )
        
        logger.info(f"File uploaded: {filename} by {user_info['username']}")
        
        return web.json_response({
            'success': True,
            'file_url': f"/api/download/{Path(file_path).name}",
            'file_name': filename,
            'file_size': len(content)
        })
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return web.json_response(
            {'error': str(e)},
            status=500
        )


async def handle_download(request: web.Request) -> web.Response:
    """
    Handle file download endpoint.
    
    GET /api/download/{filename}
    """
    config = get_config()
    filename = request.match_info.get('filename')
    
    if not filename:
        return web.json_response({'error': 'Filename required'}, status=400)
    
    # Sanitize filename
    filename = Path(filename).name
    
    file_path = Path(config.upload_dir) / filename
    
    if not file_path.exists():
        return web.json_response({'error': 'File not found'}, status=404)
    
    # Serve file
    return web.FileResponse(file_path)


async def handle_user_info(request: web.Request) -> web.Response:
    """
    Get current user information.
    
    GET /api/user
    """
    auth = get_auth_manager()
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return web.json_response({'error': 'Authentication required'}, status=401)
    
    token = auth.extract_token_from_header(auth_header)
    user_info = auth.get_user_from_token(token)
    
    if not user_info:
        return web.json_response({'error': 'Invalid token'}, status=401)
    
    return web.json_response({
        'user_id': user_info['user_id'],
        'username': user_info['username']
    })


async def handle_health(request: web.Request) -> web.Response:
    """Health check endpoint."""
    return web.json_response({'status': 'healthy', 'service': 'BaraChat'})


def setup_routes(app: web.Application):
    """Set up REST API routes."""
    app.router.add_post('/api/upload', handle_upload)
    app.router.add_get('/api/download/{filename}', handle_download)
    app.router.add_get('/api/user', handle_user_info)
    app.router.add_get('/health', handle_health)

