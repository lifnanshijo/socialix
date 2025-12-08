"""
Clips Routes - API endpoints for clips feature
Handles all HTTP requests related to clips
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.clip import Clip
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create Blueprint
clips_bp = Blueprint('clips', __name__)

# Configuration
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB max
UPLOAD_FOLDER = 'uploads/clips'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """
    Check if file extension is allowed

    Args:
        filename (str): Name of the file

    Returns:
        bool: True if allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_size_mb(file):
    """
    Get file size in MB

    Args:
        file: File object from request

    Returns:
        float: File size in MB
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size / (1024 * 1024)


@clips_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_clip():
    """
    Upload a new clip (image or short video)

    POST /api/clips/upload
    Required: clip file, user authentication
    Optional: caption

    Returns:
        json: Success/error message with clip data
    """
    try:
        current_user_id = get_jwt_identity()

        # Check if file is in request
        if 'clip' not in request.files:
            logger.warning(f"Upload attempt without file by user_id={current_user_id}")
            return jsonify({'error': 'No clip file provided'}), 400

        file = request.files['clip']
        caption = request.form.get('caption', None)

        # Validate file
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file format. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        # Check file size
        file_size_mb = get_file_size_mb(file)
        if file_size_mb > 100:
            return jsonify({'error': 'File size exceeds 100MB limit'}), 413

        # Read file data into memory
        file_data = file.read()
        file_size_bytes = len(file_data)

        # Get MIME type
        file_type = file.content_type or 'application/octet-stream'

        # Create clip in database with binary data
        clip_data = Clip.create_clip(
            current_user_id,
            file_data,
            file.filename,
            file_type,
            file_size_bytes,
            caption
        )

        if not clip_data:
            logger.error(f"Failed to save clip metadata for user_id={current_user_id}")
            return jsonify({'error': 'Failed to save clip'}), 500

        logger.info(f"Clip uploaded successfully: clip_id={clip_data['clip_id']}, user_id={current_user_id}")

        return jsonify({
            'message': 'Clip uploaded successfully',
            'clip': clip_data
        }), 201

    except Exception as e:
        logger.error(f"Error uploading clip: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@clips_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_clips(user_id):
    """
    Get all active clips of a specific user

    GET /api/clips/user/<user_id>

    Returns:
        json: List of active clips
    """
    try:
        clips = Clip.get_active_clips_by_user(user_id)

        return jsonify({
            'user_id': user_id,
            'clips': clips,
            'count': len(clips)
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving user clips: {str(e)}")
        return jsonify({'error': 'Failed to retrieve clips'}), 500


@clips_bp.route('/<int:clip_id>/download', methods=['GET'])
@jwt_required()
def download_clip(clip_id):
    """
    Download/retrieve clip file data from database
    Returns the file as an inline response so it can be displayed in browsers

    GET /api/clips/<clip_id>/download

    Returns:
        bytes: File data with appropriate content-type header
    """
    try:
        clip = Clip.get_clip_by_id(clip_id)

        if not clip:
            logger.warning(f"Download attempt for non-existent clip_id={clip_id}")
            return jsonify({'error': 'Clip not found'}), 404

        # Return file data with appropriate headers for inline display
        from flask import send_file
        from io import BytesIO

        file_stream = BytesIO(clip['file_data'])
        return send_file(
            file_stream,
            mimetype=clip['file_type'],
            as_attachment=False,  # Display inline instead of download
            download_name=clip['file_name']
        )

    except Exception as e:
        logger.error(f"Error downloading clip: {str(e)}")
        return jsonify({'error': 'Failed to download clip'}), 500


@clips_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_clips():
    """
    Get all active clips from followed users

    GET /api/clips/all

    Returns:
        json: List of active clips from followed users
    """
    try:
        current_user_id = get_jwt_identity()
        clips = Clip.get_followed_clips(current_user_id)

        return jsonify({
            'clips': clips,
            'count': len(clips)
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving followed clips: {str(e)}")
        return jsonify({'error': 'Failed to retrieve clips'}), 500


@clips_bp.route('/<int:clip_id>', methods=['DELETE'])
@jwt_required()
def delete_clip(clip_id):
    """
    Delete a clip by ID (user must own the clip)

    DELETE /api/clips/<clip_id>

    Returns:
        json: Success/error message
    """
    try:
        current_user_id = get_jwt_identity()
        current_user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id

        logger.info(f"Delete request: clip_id={clip_id}, user_id={current_user_id}")

        # Verify ownership and delete
        success = Clip.delete_clip(clip_id, current_user_id)

        if not success:
            logger.warning(f"Delete failed: clip_id={clip_id}, user_id={current_user_id}")
            return jsonify({'error': 'Clip not found or unauthorized'}), 404

        logger.info(f"Clip deleted: clip_id={clip_id}, user_id={current_user_id}")

        return jsonify({'message': 'Clip deleted successfully'}), 200

    except Exception as e:
        logger.error(f"Error deleting clip: {str(e)}")
        return jsonify({'error': 'Failed to delete clip'}), 500


@clips_bp.route('/cleanup/expired', methods=['POST'])
def cleanup_expired_clips():
    """
    Delete all expired clips from database
    This endpoint should be called by a cron job or scheduler

    POST /api/clips/cleanup/expired

    Returns:
        json: Number of clips deleted
    """
    try:
        # In production, add authentication/API key validation here
        deleted_count = Clip.delete_expired_clips()

        logger.info(f"Cleanup task completed. Deleted {deleted_count} expired clips")

        return jsonify({
            'message': 'Cleanup completed',
            'deleted_count': deleted_count
        }), 200

    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")
        return jsonify({'error': 'Cleanup failed'}), 500
