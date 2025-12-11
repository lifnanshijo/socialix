"""
Clips Model - Database ORM for clips feature
Handles all clip-related database operations
"""

from datetime import datetime, timedelta
from config.database import get_db_connection
from config.supabase_storage import upload_file_to_supabase, delete_file_from_supabase
import logging

logger = logging.getLogger(__name__)


class Clip:
    """Clip model for handling clip operations in database"""

    @staticmethod
    def create_clip(user_id, file_data, file_name, file_type, file_size, caption=None):
        """
        Create a new clip - Upload to Supabase and store URL

        Args:
            user_id (int): ID of the user uploading the clip
            file_data (bytes): Binary file data
            file_name (str): Original filename
            file_type (str): MIME type (e.g., 'image/jpeg', 'video/mp4')
            file_size (int): File size in bytes
            caption (str, optional): Caption for the clip

        Returns:
            dict: Clip data with clip_id if successful, None otherwise
        """
        try:
            # Upload to Supabase
            video_url = upload_file_to_supabase(file_data, file_type, 'clips')
            if not video_url:
                logger.error("Failed to upload clip to Supabase")
                return None
            
            conn = get_db_connection()
            cursor = conn.cursor()

            # Calculate expiration time (24 hours from now)
            created_at = datetime.now()
            expires_at = created_at + timedelta(hours=24)

            query = """
                INSERT INTO clips (user_id, video_url, file_name, file_type, file_size, caption, created_at, expires_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (user_id, video_url, file_name, file_type, file_size, caption, created_at, expires_at))
            conn.commit()

            clip_id = cursor.lastrowid

            logger.info(f"Clip created successfully: clip_id={clip_id}, user_id={user_id}")

            return {
                'clip_id': clip_id,
                'user_id': user_id,
                'video_url': video_url,
                'file_name': file_name,
                'file_type': file_type,
                'file_size': file_size,
                'caption': caption,
                'created_at': created_at.isoformat(),
                'expires_at': expires_at.isoformat()
            }

        except Exception as e:
            logger.error(f"Error creating clip: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_active_clips_by_user(user_id):
        """
        Get all active (non-expired) clips of a specific user

        Args:
            user_id (int): ID of the user

        Returns:
            list: List of active clips
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT clip_id, user_id, video_url, file_name, file_type, file_size, caption, created_at, expires_at
                FROM clips
                WHERE user_id = %s AND expires_at > NOW() AND is_deleted = FALSE
                ORDER BY created_at DESC
            """

            cursor.execute(query, (user_id,))
            clips = cursor.fetchall()

            result = []
            for clip in clips:
                result.append({
                    'clip_id': clip[0],
                    'user_id': clip[1],
                    'video_url': clip[2],
                    'file_name': clip[3],
                    'file_type': clip[4],
                    'file_size': clip[5],
                    'caption': clip[6],
                    'created_at': clip[7].isoformat(),
                    'expires_at': clip[8].isoformat()
                })

            logger.info(f"Retrieved {len(result)} active clips for user_id={user_id}")
            return result

        except Exception as e:
            logger.error(f"Error retrieving clips for user: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_followed_clips(user_id):
        """
        Get all active clips from users that the current user follows

        Args:
            user_id (int): ID of the current user

        Returns:
            list: List of active clips from followed users
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT c.clip_id, c.user_id, c.video_url, c.file_name, c.file_type, c.file_size, c.caption, c.created_at, c.expires_at, u.username
                FROM clips c
                INNER JOIN followers f ON c.user_id = f.following_id
                INNER JOIN users u ON c.user_id = u.id
                WHERE f.follower_id = %s AND c.expires_at > NOW() AND c.is_deleted = FALSE
                ORDER BY c.created_at DESC
            """

            cursor.execute(query, (user_id,))
            clips = cursor.fetchall()

            result = []
            for clip in clips:
                result.append({
                    'clip_id': clip[0],
                    'user_id': clip[1],
                    'video_url': clip[2],
                    'file_name': clip[3],
                    'file_type': clip[4],
                    'file_size': clip[5],
                    'caption': clip[6],
                    'created_at': clip[7].isoformat(),
                    'expires_at': clip[8].isoformat(),
                    'uploaded_by': clip[9]
                })

            logger.info(f"Retrieved {len(result)} clips from followed users for user_id={user_id}")
            return result

        except Exception as e:
            logger.error(f"Error retrieving followed clips: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_clip(clip_id, user_id=None):
        """
        Delete a clip by clip_id
        If user_id is provided, verify ownership before deletion

        Args:
            clip_id (int): ID of the clip to delete
            user_id (int, optional): ID of the user (for permission check)

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # If user_id provided, verify ownership
            if user_id:
                verify_query = "SELECT user_id FROM clips WHERE clip_id = %s"
                cursor.execute(verify_query, (clip_id,))
                clip = cursor.fetchone()

                if not clip or clip[0] != user_id:
                    logger.warning(f"Unauthorized deletion attempt: clip_id={clip_id}, user_id={user_id}")
                    return False

            # Delete the clip
            delete_query = "DELETE FROM clips WHERE clip_id = %s"
            cursor.execute(delete_query, (clip_id,))
            conn.commit()

            logger.info(f"Clip deleted successfully: clip_id={clip_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting clip: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_expired_clips():
        """
        Delete all expired clips from the database
        This should be called by a scheduled task (cron job)

        Returns:
            int: Number of clips deleted
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "DELETE FROM clips WHERE expires_at <= NOW()"
            cursor.execute(query)
            conn.commit()

            deleted_count = cursor.rowcount
            logger.info(f"Deleted {deleted_count} expired clips")

            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting expired clips: {str(e)}")
            return 0
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_clip_by_id(clip_id):
        """
        Get a specific clip by its ID with binary data

        Args:
            clip_id (int): ID of the clip

        Returns:
            dict: Clip data including file_data if found, None otherwise
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT clip_id, user_id, file_data, file_name, file_type, file_size, caption, created_at, expires_at
                FROM clips
                WHERE clip_id = %s AND expires_at > NOW() AND is_deleted = FALSE
            """

            cursor.execute(query, (clip_id,))
            clip = cursor.fetchone()

            if not clip:
                return None

            return {
                'clip_id': clip[0],
                'user_id': clip[1],
                'file_data': clip[2],
                'file_name': clip[3],
                'file_type': clip[4],
                'file_size': clip[5],
                'caption': clip[6],
                'created_at': clip[7].isoformat(),
                'expires_at': clip[8].isoformat()
            }

        except Exception as e:
            logger.error(f"Error retrieving clip: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
