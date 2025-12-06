# Clips (Stories) Feature - Backend Configuration

"""
Clips module configuration for Flask app
Handles all imports and initialization
"""

from flask import Blueprint

# Create Blueprint for clips routes
clips_bp = Blueprint('clips', __name__)

# Import routes (will be created)
from routes.clip_routes import clips_bp

__all__ = ['clips_bp']
