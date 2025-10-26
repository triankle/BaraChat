"""SFU (Selective Forwarding Unit) stub for future implementation."""

from server.utils.logger import get_logger


logger = get_logger(__name__)


class SFU:
    """
    Selective Forwarding Unit for advanced voice routing.
    
    This is a stub for future SFU implementation.
    An SFU would forward media streams between peers efficiently.
    """
    
    def __init__(self):
        """Initialize the SFU."""
        pass
    
    async def start(self):
        """Start the SFU server."""
        logger.info("SFU: Not yet implemented")
        pass
    
    async def stop(self):
        """Stop the SFU server."""
        logger.info("SFU: Stopping")
        pass

