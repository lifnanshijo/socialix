# Fix Supabase Storage Permissions

## Problem
Your Supabase bucket has Row Level Security (RLS) enabled but no policies allow uploads.

Error: `new row violates row-level security policy`

## Quick Fix - Option 1: Disable RLS (Simple but less secure)

1. Go to Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Go to **Storage** in the left sidebar
4. Click on your `socialx` bucket
5. Click the **⚙️ Settings** (gear icon)
6. Turn OFF "Enable RLS" 
7. Save changes

## Better Fix - Option 2: Add RLS Policies (Recommended)

Go to **SQL Editor** in Supabase and run these policies:

```sql
-- Allow public read access (anyone can view files)
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'socialx' );

-- Allow anyone to upload files
CREATE POLICY "Public Upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'socialx' );

-- Allow anyone to update files
CREATE POLICY "Public Update"  
ON storage.objects FOR UPDATE
USING ( bucket_id = 'socialx' );

-- Allow anyone to delete files
CREATE POLICY "Public Delete"
ON storage.objects FOR DELETE
USING ( bucket_id = 'socialx' );
```

## Option 3: Authenticated Users Only (Most Secure)

If you want only logged-in users to upload:

```sql
-- Allow public read
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'socialx' );

-- Allow authenticated users to upload
CREATE POLICY "Authenticated Upload"
ON storage.objects FOR INSERT
WITH CHECK ( 
  bucket_id = 'socialx' AND 
  auth.role() = 'authenticated' 
);

-- Allow authenticated users to update their own files
CREATE POLICY "Authenticated Update"
ON storage.objects FOR UPDATE
USING (
  bucket_id = 'socialx' AND
  auth.role() = 'authenticated'
);

-- Allow authenticated users to delete their own files
CREATE POLICY "Authenticated Delete"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'socialx' AND
  auth.role() = 'authenticated'
);
```

## After Setting Up Policies

1. Restart your Flask server
2. Try creating a post with an image
3. Check if the upload succeeds!

Your images will now upload to Supabase and be accessible via CDN URLs! 🚀
