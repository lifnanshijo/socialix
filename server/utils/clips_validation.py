"""
Clips Validation Module - Input validation and error handling
Validates clip uploads and requests
"""

import os
from functools import wraps
from flask import jsonify, request
import logging

logger = logging.getLogger(__name__)

# Configuration
ALLOWED_VIDEO_FORMATS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv'}
ALLOWED_IMAGE_FORMATS = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'}
ALLOWED_FORMATS = ALLOWED_VIDEO_FORMATS | ALLOWED_IMAGE_FORMATS

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_CAPTION_LENGTH = 500
MIN_CAPTION_LENGTH = 0


class ClipValidationError(Exception):
    """Custom exception for clip validation errors"""
    pass


def validate_file_extension(filename):
    """
    Validate file extension

    Args:
        filename (str): Name of the file

    Returns:
        tuple: (is_valid, error_message)
    """
    if '.' not in filename:
        return False, "File must have an extension"

    ext = filename.rsplit('.', 1)[1].lower()

    if ext not in ALLOWED_FORMATS:
        return False, f"File format '.{ext}' not allowed. Allowed: {', '.join(ALLOWED_FORMATS)}"

    return True, None


def validate_file_size(file):
    """
    Validate file size

    Args:
        file: File object from request

    Returns:
        tuple: (is_valid, error_message, size_in_mb)
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    size_mb = size / (1024 * 1024)

    if size == 0:
        return False, "File is empty", 0

    if size > MAX_FILE_SIZE:
        return False, f"File size ({size_mb:.2f}MB) exceeds maximum ({MAX_FILE_SIZE / (1024 * 1024):.0f}MB)", size_mb

    return True, None, size_mb


def validate_caption(caption):
    """
    Validate clip caption

    Args:
        caption (str): Caption text

    Returns:
        tuple: (is_valid, error_message)
    """
    if caption is None:
        return True, None

    caption = str(caption).strip()

    if len(caption) < MIN_CAPTION_LENGTH:
        return False, f"Caption must be at least {MIN_CAPTION_LENGTH} characters"

    if len(caption) > MAX_CAPTION_LENGTH:
        return False, f"Caption cannot exceed {MAX_CAPTION_LENGTH} characters (current: {len(caption)})"

    # Check for malicious content
    if '<script>' in caption.lower() or 'javascript:' in caption.lower():
        return False, "Caption contains invalid content"

    return True, None


def validate_clip_upload(f):
    """
    Decorator to validate clip upload request
    Checks file, caption, and other requirements

    Usage:
        @app.route('/upload', methods=['POST'])
        @validate_clip_upload
        def upload_clip():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Check if file exists
            if 'clip' not in request.files:
                logger.warning("Upload attempt without file")
                return jsonify({'error': 'No clip file provided'}), 400

            file = request.files['clip']

            if file.filename == '':
                logger.warning("Upload attempt with empty filename")
                return jsonify({'error': 'No file selected'}), 400

            # Validate extension
            is_valid, error = validate_file_extension(file.filename)
            if not is_valid:
                logger.warning(f"Invalid file format: {file.filename}")
                return jsonify({'error': error}), 400

            # Validate file size
            is_valid, error, size_mb = validate_file_size(file)
            if not is_valid:
                logger.warning(f"Invalid file size: {size_mb}MB")
                return jsonify({'error': error}), 413

            # Validate caption if provided
            caption = request.form.get('caption', '').strip()
            is_valid, error = validate_caption(caption)
            if not is_valid:
                logger.warning(f"Invalid caption: {error}")
                return jsonify({'error': error}), 400

            # Store validation results in request context
            request.validated_file = file
            request.validated_caption = caption if caption else None

            return f(*args, **kwargs)

        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify({'error': 'Validation failed'}), 400

    return decorated_function


def get_file_type_from_extension(filename):
    """
    Get MIME type from filename extension

    Args:
        filename (str): Name of the file

    Returns:
        str: MIME type or 'unknown'
    """
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    mime_types = {
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'mkv': 'video/x-matroska',
        'webm': 'video/webm',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
    }

    return mime_types.get(ext, 'unknown')


def is_video_file(filename):
    """Check if file is a video"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in ALLOWED_VIDEO_FORMATS


def is_image_file(filename):
    """Check if file is an image"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in ALLOWED_IMAGE_FORMATS
