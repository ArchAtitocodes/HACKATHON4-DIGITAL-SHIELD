"""
Routes package for Digital Shield
Contains API endpoints for chatbot, literacy guide, and health checks
"""

from .chatbot import chatbot_bp
from .literacy import literacy_bp
from .health import health_bp

__all__ = ['chatbot_bp', 'literacy_bp', 'health_bp']