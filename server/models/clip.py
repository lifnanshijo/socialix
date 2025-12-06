"""
Clips Model - Database ORM for clips feature
Handles all clip-related database operations
"""

from datetime import datetime, timedelta
from config.database import get_db_connection
import logging

logger = logging.getLogger(__name__)


class Clip:
    """Clip model for handling clip operations in database"""

    @staticmethod
    def create_clip(user_id, file_url, caption=None):
        """
        Create a new clip in the database

        Args:
            user_id (int): ID of the user uploading the clip
            file_url (str): URL/path to the clip file
            caption (str, optional): Caption for the clip

        Returns:
            dict: Clip data with clip_id if successful, None otherwise
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Calculate expiration time (24 hours from now)
            created_at = datetime.now()
            expires_at = created_at + timedelta(hours=24)

            query = """
                INSERT INTO clips (user_id, file_url, caption, created_at, expires_at)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (user_id, file_url, caption, created_at, expires_at))
            conn.commit()

            clip_id = cursor.lastrowid

            logger.info(f"Clip created successfully: clip_id={clip_id}, user_id={user_id}")

            return {
                'clip_id': clip_id,
                'user_id': user_id,
                'file_url': file_url,
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
                SELECT clip_id, user_id, file_url, caption, created_at, expires_at
                FROM clips
                WHERE user_id = %s AND expires_at > NOW()
                ORDER BY created_at DESC
            """

            cursor.execute(query, (user_id,))
            clips = cursor.fetchall()

            result = []
            for clip in clips:
                result.append({
                    'clip_id': clip[0],
                    'user_id': clip[1],
                    'file_url': clip[2],
                    'caption': clip[3],
                    'created_at': clip[4].isoformat(),
                    'expires_at': clip[5].isoformat()
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
                SELECT c.clip_id, c.user_id, c.file_url, c.caption, c.created_at, c.expires_at, u.username
                FROM clips c
                INNER JOIN follows f ON c.user_id = f.followed_user_id
                INNER JOIN users u ON c.user_id = u.id
                WHERE f.follower_user_id = %s AND c.expires_at > NOW()
                ORDER BY c.created_at DESC
            """

            cursor.execute(query, (user_id,))
            clips = cursor.fetchall()

            result = []
            for clip in clips:
                result.append({
                    'clip_id': clip[0],
                    'user_id': clip[1],
                    'file_url': clip[2],
                    'caption': clip[3],
                    'created_at': clip[4].isoformat(),
                    'expires_at': clip[5].isoformat(),
                    'uploaded_by': clip[6]
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
        Get a specific clip by its ID

        Args:
            clip_id (int): ID of the clip

        Returns:
            dict: Clip data if found, None otherwise
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                SELECT clip_id, user_id, file_url, caption, created_at, expires_at
                FROM clips
                WHERE clip_id = %s AND expires_at > NOW()
            """

            cursor.execute(query, (clip_id,))
            clip = cursor.fetchone()

            if not clip:
                return None

            return {
                'clip_id': clip[0],
                'user_id': clip[1],
                'file_url': clip[2],
                'caption': clip[3],
                'created_at': clip[4].isoformat(),
                'expires_at': clip[5].isoformat()
            }

        except Exception as e:
            logger.error(f"Error retrieving clip: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()
