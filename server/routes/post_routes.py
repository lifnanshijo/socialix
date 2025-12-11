from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models.post import Post
from models.user import User
from models.interactions import Like, Comment
from models.notification import Notification
from middleware.auth import token_required
import mimetypes

post_bp = Blueprint('posts', __name__)

# Configuration
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB

def allowed_image_file(filename):
    """Check if image file type is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_video_file(filename):
    """Check if video file type is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def get_mime_type(filename, file_type='image'):
    """Get MIME type of file"""
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        return mime_type
    if file_type == 'image':
        return 'image/jpeg'
    else:
        return 'video/mp4'

def read_media_to_blob(file, file_type='image'):
    """Read media file and return binary data with MIME type"""
    if not file or file.filename == '':
        return None, None
    
    if file_type == 'image':
        if not allowed_image_file(file.filename):
            raise ValueError('Image type not allowed. Use: PNG, JPG, JPEG, GIF, WebP')
        max_size = MAX_IMAGE_SIZE
    elif file_type == 'video':
        if not allowed_video_file(file.filename):
            raise ValueError('Video type not allowed. Use: MP4, AVI, MOV, MKV, WebM')
        max_size = MAX_VIDEO_SIZE
    else:
        raise ValueError('Invalid file type')
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Seek to start
    
    if file_size > max_size:
        size_limit = f"{max_size // (1024*1024)}MB"
        raise ValueError(f'File size exceeds {size_limit} limit')
    
    # Read file content as bytes
    media_data = file.read()
    mime_type = get_mime_type(file.filename, file_type)
    
    return media_data, mime_type

@post_bp.route('/create', methods=['POST'])
@token_required
def create_post():
    """Create a new post with optional image or video (stored as BLOB)"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Get form data
        content = request.form.get('content', '').strip()
        media_type = 'text'
        image_data = None
        image_type = None
        video_data = None
        video_type = None
        
        # Check if image was uploaded
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                image_data, image_type = read_media_to_blob(image_file, 'image')
                if image_data:
                    media_type = 'image'
        
        # Check if video was uploaded
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file and video_file.filename:
                video_data, video_type = read_media_to_blob(video_file, 'video')
                if video_data:
                    media_type = 'video'
        
        # Validate post has content or media
        if not content and not image_data and not video_data:
            return jsonify({'message': 'Post must have content or media'}), 400
        
        # Create post with BLOB data
        post = Post.create(
            user_id, 
            content, 
            image_data=image_data,
            image_type=image_type,
            video_data=video_data,
            video_type=video_type,
            media_type=media_type
        )
        
        if not post:
            return jsonify({'message': 'Failed to create post'}), 500
        
        # Get user information
        user = User.find_by_id(user_id)
        post_data = Post.to_dict(post)
        post_data['user'] = User.to_dict(user) if user else None
        
        return jsonify(post_data), 201
    except ValueError as e:
        print(f"Validation error in create_post: {e}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        print(f"Error in create_post: {e}")
        return jsonify({'message': str(e)}), 500

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a post by ID"""
    try:
        post = Post.find_by_id(post_id)
        
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        
        # Get user info
        user = User.find_by_id(post['user_id'])
        post_data = Post.to_dict(post)
        post_data['user'] = User.to_dict(user) if user else None
        
        return jsonify(post_data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@post_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    """Get all posts by a specific user"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = 20
        offset = (page - 1) * limit
        
        posts = Post.find_by_user(user_id, limit, offset)
        
        if not posts:
            return jsonify([]), 200
        
        # Get user info
        user = User.find_by_id(user_id)
        posts_data = []
        for post in posts:
            post_data = Post.to_dict(post)
            post_data['user'] = User.to_dict(user) if user else None
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@post_bp.route('/feed', methods=['GET'])
def get_feed():
    """Get feed of all posts or posts by specific user"""
    try:
        page = request.args.get('page', 1, type=int)
        user_id = request.args.get('user_id', type=int)
        limit = 20
        offset = (page - 1) * limit
        
        if user_id:
            # Get posts by specific user
            posts = Post.get_user_posts(user_id, limit, offset)
        else:
            # Get all posts
            posts = Post.get_feed(limit, offset)
        
        if not posts:
            return jsonify({'posts': []}), 200
        
        posts_data = []
        for post in posts:
            post_data = Post.to_dict(post)
            user = User.find_by_id(post['user_id'])
            post_data['user'] = User.to_dict(user) if user else None
            posts_data.append(post_data)
        
        return jsonify({'posts': posts_data}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@post_bp.route('/<int:post_id>', methods=['PUT'])
@token_required
def update_post(post_id):
    """Update a post"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        post = Post.find_by_id(post_id)
        
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        
        # Check if user owns the post
        if post['user_id'] != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        # Get form data
        content = request.form.get('content')
        image_data = post.get('image_data')
        image_type = post.get('image_type')
        video_data = post.get('video_data')
        video_type = post.get('video_type')
        
        # Handle new image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename:
                new_image_data, new_image_type = read_media_to_blob(image_file, 'image')
                if new_image_data:
                    image_data = new_image_data
                    image_type = new_image_type
        
        # Handle new video upload
        if 'video' in request.files:
            video_file = request.files['video']
            if video_file and video_file.filename:
                new_video_data, new_video_type = read_media_to_blob(video_file, 'video')
                if new_video_data:
                    video_data = new_video_data
                    video_type = new_video_type
        
        # Update post
        updated_post = Post.update(
            post_id, 
            content=content,
            image_data=image_data,
            image_type=image_type,
            video_data=video_data,
            video_type=video_type
        )
        
        if not updated_post:
            return jsonify({'message': 'Failed to update post'}), 500
        
        return jsonify(Post.to_dict(updated_post)), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(post_id):
    """Delete a post"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        post = Post.find_by_id(post_id)
        
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        
        # Check if user owns the post
        if post['user_id'] != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        Post.delete(post_id)
        
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Like endpoints
@post_bp.route('/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(post_id):
    """Like a post"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Check if post exists
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        
        # Add like
        success = Like.add_like(user_id, post_id)
        if not success:
            return jsonify({'message': 'Already liked'}), 400
        
        # Create notification for post owner (if not liking own post)
        if post['user_id'] != user_id:
            current_user = User.find_by_id(user_id)
            if current_user:
                Notification.create_notification(
                    user_id=post['user_id'],
                    sender_id=user_id,
                    notification_type='like',
                    content=f"{current_user['username']} liked your post",
                    reference_id=post_id
                )
        
        like_count = Like.get_like_count(post_id)
        
        return jsonify({
            'message': 'Post liked',
            'likeCount': like_count,
            'isLiked': True
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@post_bp.route('/<int:post_id>/unlike', methods=['POST'])
@token_required
def unlike_post(post_id):
    """Unlike a post"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Remove like
        Like.remove_like(user_id, post_id)
        like_count = Like.get_like_count(post_id)
        
        return jsonify({
            'message': 'Post unliked',
            'likeCount': like_count,
            'isLiked': False
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@post_bp.route('/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    """Get all likes for a post"""
    try:
        likes = Like.get_post_likes(post_id)
        like_count = Like.get_like_count(post_id)
        
        return jsonify({
            'count': like_count,
            'likes': likes
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Comment endpoints
@post_bp.route('/<int:post_id>/comments', methods=['POST'])
@token_required
def add_comment(post_id):
    """Add a comment to a post"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'message': 'Comment content is required'}), 400
        
        # Check if post exists
        post = Post.find_by_id(post_id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404
        
        # Create comment
        comment = Comment.create(user_id, post_id, content)
        
        if not comment:
            return jsonify({'message': 'Failed to create comment'}), 500
        
        # Create notification for post owner (if not commenting on own post)
        if post['user_id'] != user_id:
            current_user = User.find_by_id(user_id)
            if current_user:
                Notification.create_notification(
                    user_id=post['user_id'],
                    sender_id=user_id,
                    notification_type='comment',
                    content=f"{current_user['username']} commented on your post",
                    reference_id=post_id
                )
        
        return jsonify(Comment.to_dict(comment)), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@post_bp.route('/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Get all comments for a post"""
    try:
        comments = Comment.find_by_post(post_id)
        comment_count = Comment.get_comment_count(post_id)
        
        return jsonify({
            'count': comment_count,
            'comments': [Comment.to_dict(comment) for comment in comments]
        }), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@post_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(comment_id):
    """Delete a comment"""
    try:
        user_id = get_jwt_identity()
        user_id = int(user_id) if isinstance(user_id, str) else user_id
        
        # Check if comment exists
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({'message': 'Comment not found'}), 404
        
        # Check if user owns the comment
        if comment['user_id'] != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        Comment.delete(comment_id, user_id)
        
        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
