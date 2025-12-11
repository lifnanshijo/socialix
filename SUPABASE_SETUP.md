# Supabase Storage Setup Guide

This guide will help you set up Supabase for storing images and videos.

## 1. Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in the details:
   - Project name: `social-media` (or your preferred name)
   - Database password: (save this securely)
   - Region: Choose closest to your users
5. Wait for the project to be created (~2 minutes)

## 2. Create a Storage Bucket

1. In your Supabase dashboard, go to **Storage** (in the left sidebar)
2. Click **New Bucket**
3. Bucket details:
   - Name: `social-media-files` (or match your `.env` SUPABASE_BUCKET value)
   - **Public bucket**: ✅ Check this box (so files are publicly accessible)
4. Click **Create Bucket**

## 3. Get Your Supabase Credentials

1. Go to **Project Settings** (gear icon in sidebar)
2. Click **API** in the sidebar
3. You'll see:
   - **Project URL**: Copy this (looks like `https://xxxxx.supabase.co`)
   - **Project API keys** → **anon/public**: Copy this key

## 4. Update Your .env File

Add these variables to your `server/.env` file:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key-here
SUPABASE_BUCKET=social-media-files
```

Replace:
- `your-project-id` with your actual project ID from the URL
- `your-anon-public-key-here` with the anon/public key you copied

## 5. Install Python Dependencies

```bash
cd server
pip install -r requirements.txt
```

This will install the `supabase` Python package.

## 6. Run Database Migration

Run the migration script to update your database schema from BLOB to URL storage:

```bash
cd server
python migrate_to_supabase.py
```

Type `yes` when prompted to confirm the migration.

**Note**: This will:
- Backup your existing data to `*_backup` tables
- Convert BLOB columns to VARCHAR(500) for URLs
- Remove the `_type` columns (e.g., `avatar_type`, `image_type`)

## 7. Folder Structure in Supabase

Files will be organized in folders:
- `avatars/` - User profile pictures
- `covers/` - User cover images
- `posts/` - Post images and videos
- `clips/` - Clip videos (24-hour stories)

## 8. File Naming Convention

Files are automatically named with:
- Timestamp (YYYYMMDD_HHMMSS)
- Unique ID (8 characters)
- Original file extension

Example: `posts/20251211_143022_a1b2c3d4.jpg`

## 9. Security & Policies (Optional)

For better security, you can set up Row Level Security (RLS) policies:

1. Go to **Storage** → **Policies** in Supabase
2. Add policies for your bucket:
   - **SELECT**: Allow public read access
   - **INSERT**: Allow authenticated users to upload
   - **UPDATE**: Allow users to update their own files
   - **DELETE**: Allow users to delete their own files

Example policy for SELECT:
```sql
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'social-media-files' );
```

Example policy for INSERT (authenticated users):
```sql
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'social-media-files' AND auth.role() = 'authenticated' );
```

## 10. Test the Setup

After migration, test by:
1. Start your server: `python app.py`
2. Upload a profile picture through your app
3. Check Supabase Storage to see if the file appears
4. Verify the URL is stored in your MySQL database

## Troubleshooting

### Issue: "Supabase client not initialized"
- Check that SUPABASE_URL and SUPABASE_KEY are set in `.env`
- Restart your server after adding the variables

### Issue: "Upload failed"
- Verify the bucket name matches in `.env` and Supabase
- Check that the bucket is set to **Public**
- Verify your Supabase key is correct

### Issue: Images not displaying
- Check browser console for CORS errors
- Verify the bucket has public access enabled
- Check the URL format in database

## Benefits of Supabase Storage

✅ **Automatic CDN** - Fast global delivery
✅ **Unlimited storage** - Pay as you grow  
✅ **Built-in optimization** - Automatic image resizing
✅ **Security** - Fine-grained access control with RLS
✅ **No server load** - Media served directly from Supabase
✅ **Backup** - Built-in redundancy

## Cost

Supabase Free Tier includes:
- 1 GB storage
- 2 GB bandwidth/month

Upgrade to Pro ($25/month) for:
- 100 GB storage
- 200 GB bandwidth/month

Perfect for starting your social media app! 🚀
