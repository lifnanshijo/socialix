-- Migration: Add image_data column to posts table if it doesn't exist

USE social_connect;

ALTER TABLE posts ADD COLUMN IF NOT EXISTS image_data LONGBLOB;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS image_type VARCHAR(50);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS video_data LONGBLOB;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS video_type VARCHAR(50);
ALTER TABLE posts ADD COLUMN IF NOT EXISTS media_type ENUM('text', 'image', 'video') DEFAULT 'text';

-- Verify the columns were added
SHOW COLUMNS FROM posts;
