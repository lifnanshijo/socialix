"""
Clips Database Schema - MySQL table creation and migration
Run this to create the clips table in your database
"""

# SQL Query to create the clips table
CREATE_CLIPS_TABLE = """
CREATE TABLE IF NOT EXISTS clips (
    clip_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    caption VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    
    -- Foreign key relationship with users table
    CONSTRAINT fk_clips_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes for better query performance
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_created_at (created_at),
    INDEX idx_active_clips (expires_at, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

# Alternative table creation with additional fields for extended features
CREATE_CLIPS_TABLE_EXTENDED = """
CREATE TABLE IF NOT EXISTS clips (
    clip_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INT,  -- File size in bytes
    file_type VARCHAR(50),  -- e.g., 'image/jpeg', 'video/mp4'
    caption VARCHAR(500),
    views_count INT DEFAULT 0,  -- Number of views
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,  -- Soft delete flag
    
    -- Foreign key relationship with users table
    CONSTRAINT fk_clips_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes for better query performance
    INDEX idx_user_id (user_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_created_at (created_at),
    INDEX idx_active_clips (expires_at, is_deleted),
    INDEX idx_deleted_flag (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def create_clips_table(connection):
    """
    Execute the CREATE TABLE query to set up clips table
    
    Args:
        connection: MySQL database connection object
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_CLIPS_TABLE)
        connection.commit()
        print("✓ Clips table created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating clips table: {str(e)}")
        return False
    finally:
        cursor.close()


# Migration script to add clips table to existing database
MIGRATION_SCRIPT = """
-- Drop existing table if needed (USE WITH CAUTION)
-- DROP TABLE IF EXISTS clips;

-- Create clips table
{CREATE_CLIPS_TABLE}

-- Create indexes for performance
ALTER TABLE clips ADD INDEX idx_user_clips (user_id, expires_at);
ALTER TABLE clips ADD INDEX idx_active_clips_time (expires_at, created_at);

-- Verify table creation
DESCRIBE clips;
"""

if __name__ == '__main__':
    print(CREATE_CLIPS_TABLE)
