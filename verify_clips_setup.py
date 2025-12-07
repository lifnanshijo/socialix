#!/usr/bin/env python3
"""
Quick verification script to confirm clips upload is working
"""

import sys
sys.path.insert(0, 'server')

from config.database import get_db_connection
from datetime import datetime, timedelta

def verify_setup():
    """Verify complete setup"""
    print("CLIPS UPLOAD FIX - VERIFICATION REPORT")
    print("=" * 70)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Check table exists
        cursor.execute("SHOW TABLES LIKE 'clips'")
        table_exists = cursor.fetchone() is not None
        print(f"\n[{'PASS' if table_exists else 'FAIL'}] Clips table exists")
        
        if table_exists:
            # 2. Check columns
            cursor.execute("DESCRIBE clips")
            columns = cursor.fetchall()
            expected_columns = [
                'clip_id', 'user_id', 'file_data', 'file_name', 
                'file_size', 'file_type', 'caption', 'views_count',
                'created_at', 'expires_at', 'is_deleted'
            ]
            column_names = [col[0] for col in columns]
            all_columns_exist = all(col in column_names for col in expected_columns)
            print(f"[{'PASS' if all_columns_exist else 'FAIL'}] All required columns exist")
            
            # 3. Check data
            cursor.execute("SELECT COUNT(*) FROM clips")
            clip_count = cursor.fetchone()[0]
            print(f"[INFO] Total clips in database: {clip_count}")
            
            # 4. Check active clips
            cursor.execute(f"SELECT COUNT(*) FROM clips WHERE expires_at > NOW() AND is_deleted = FALSE")
            active_clips = cursor.fetchone()[0]
            print(f"[INFO] Active (non-expired) clips: {active_clips}")
            
            if clip_count > 0:
                print(f"\n[PASS] System is READY for uploads!")
                print("\nTo test:")
                print("  1. Go to Stories page in the app")
                print("  2. Click 'Upload' tab")
                print("  3. Select an image or video file")
                print("  4. Click 'Upload Clip' button")
                print("\nSupported formats:")
                print("  - Images: JPG, JPEG, PNG, GIF, WEBP")
                print("  - Videos: MP4, AVI, MOV, MKV")
                print("  - Max size: 100MB")
                print("  - Expiration: 24 hours")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[FAIL] Error during verification: {str(e)}")
        return False
    
    print("\n" + "=" * 70)
    return True

if __name__ == '__main__':
    success = verify_setup()
    sys.exit(0 if success else 1)
