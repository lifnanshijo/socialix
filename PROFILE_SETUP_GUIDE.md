# Profile Upload Feature - Complete Setup & Testing Guide

## Current Status
✅ Backend API endpoints created  
✅ Frontend components updated  
✅ Image upload functionality implemented  
✅ Drag-and-drop feature added  
✅ Error handling improved  

## How to Use the Profile Photo Upload Feature

### Step 1: Sign Up / Login
1. Go to http://localhost:3000
2. Click **Sign Up** and create a new account
3. Fill in username, email, and password
4. Log in with your credentials

### Step 2: Go to Your Profile
1. After login, click your profile icon or go to `/profile`
2. Click the **"Edit Profile"** button

### Step 3: Upload Photos
You now have two options:

#### Option A: Drag and Drop
1. **For Avatar (Profile Picture)**:
   - Drag your image file onto the circular upload area labeled "Profile Picture"
   - The image will preview immediately

2. **For Cover Image**:
   - Drag your image file onto the rectangular upload area labeled "Cover Image"
   - The image will preview immediately

#### Option B: Click to Select
1. **For Avatar**:
   - Click the upload area under "Profile Picture"
   - Select an image file from your computer
   - The image will preview immediately

2. **For Cover Image**:
   - Click the upload area under "Cover Image"
   - Select an image file from your computer
   - The image will preview immediately

### Step 4: Hover Over Images to Change
- Hover over the image preview to see a "Change" button
- Click it to upload a different image

### Step 5: Edit Other Profile Details
- Update your **Username** (if needed)
- Update your **Bio** with a description
- Click **"Save Changes"** to save

## Supported Image Formats
✓ PNG  
✓ JPG / JPEG  
✓ GIF  
✓ WebP  

## File Size Limit
- Maximum: **5MB per image**
- If file is too large, you'll see an error message

## Troubleshooting

### Issue: "Upload failed" Error
**Solution**: 
- Make sure you're logged in (check if token is in localStorage)
- Try uploading a smaller file
- Refresh the page and try again

### Issue: Images not showing after upload
**Solution**:
- Check browser console (F12 > Console tab) for errors
- Make sure the backend server is running on port 5000
- Try refreshing the page

### Issue: Profile edit not working
**Solution**:
- Make sure you filled in the required fields
- Check the error message that appears
- Try logging out and back in

### Issue: Can't select files
**Solution**:
- Try a different browser (Chrome, Firefox, Safari)
- Clear browser cache
- Check browser console for JavaScript errors

## Files Modified/Created

### Backend
- `/server/routes/user_routes.py` - Added upload endpoints
  - `POST /api/users/profile/upload-avatar`
  - `POST /api/users/profile/upload-cover`

### Frontend
- `/client/src/components/ProfileCustomization.jsx` - Enhanced with file upload UI
- `/client/src/pages/Profile.jsx` - Integrated upload functionality
- `/client/src/styles/profile.css` - Added styling for upload areas

### Image Storage
- `/server/uploads/avatars/` - Avatar images stored here
- `/server/uploads/covers/` - Cover images stored here

## Technical Details

### Image Upload Flow
1. User selects/drags image
2. Preview shows in real-time
3. File is automatically uploaded to server
4. Server validates file (type, size)
5. File is saved with timestamp filename
6. Database is updated with new image path
7. Profile displays updated image

### API Endpoints

**Upload Avatar:**
```
POST /api/users/profile/upload-avatar
Headers: Authorization: Bearer {token}
Body: FormData with 'file' field
```

**Upload Cover:**
```
POST /api/users/profile/upload-cover
Headers: Authorization: Bearer {token}
Body: FormData with 'file' field
```

**Update Profile:**
```
PUT /api/users/profile
Headers: Authorization: Bearer {token}
Body: JSON {username, bio}
```

## Next Steps (Optional Enhancements)

- [ ] Add image cropping tool
- [ ] Add image filters
- [ ] Add image compression
- [ ] Add photo gallery
- [ ] Add CDN integration
- [ ] Add image optimization
