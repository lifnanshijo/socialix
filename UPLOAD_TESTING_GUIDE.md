# Image Upload Troubleshooting & Testing Guide

## ✅ Simplified Upload Implementation

I've simplified the ProfileCustomization component to remove complex drag-drop logic and focus on core functionality.

### What Changed:
1. **Removed drag-and-drop handlers** - Simplified to basic click-to-upload
2. **Added explicit Authorization headers** - Ensures token is sent with upload requests
3. **Added error logging** - Better error messages for debugging
4. **Fixed axios configuration** - Proper FormData handling

## Step-by-Step Testing

### 1. Sign Up
```
URL: http://localhost:3000
1. Click "Sign Up"
2. Enter:
   - Username: testuser
   - Email: test@example.com
   - Password: password123
3. Click "Create Account"
```

### 2. You should be redirected to home or profile

### 3. Navigate to Profile
```
Click your profile icon or go to: http://localhost:3000/profile
```

### 4. Click "Edit Profile"
You should see:
- Profile Picture upload area (circle)
- Cover Image upload area (rectangle)
- Username field
- Bio field
- Save Changes button

### 5. Upload Profile Picture
```
1. Click the circular upload area under "Profile Picture"
2. Select an image file from your computer
3. You should see:
   - A preview of the image
   - A success message: "Profile picture uploaded successfully!"
   - The image displayed in the preview
```

### 6. Upload Cover Image
```
1. Click the rectangular upload area under "Cover Image"
2. Select an image file from your computer
3. You should see the same success flow as above
```

### 7. Edit Other Fields
```
1. Change the Username if desired
2. Add a Bio
3. Click "Save Changes"
4. You should see a success message
```

## Debugging Checklist

### ✓ Frontend Console (F12 > Console)
Look for logs like:
```
Token: Present
Uploading to: /api/users/profile/upload-avatar
Upload response: {message: "Avatar uploaded successfully", user: {...}}
```

### ✓ Backend Console (Terminal)
Look for:
```
Auth Header: Bearer <token_here>
POST /api/users/profile/upload-avatar HTTP/1.1" 200 -
```

### Common Issues & Fixes

**Issue: "Token is invalid or expired"**
- [ ] Make sure you're logged in
- [ ] Check localStorage in browser (F12 > Application > LocalStorage)
- [ ] Token should be there with key "token"
- [ ] Try logging out and logging back in

**Issue: "No file provided"**
- [ ] Make sure you selected a file
- [ ] File size should be under 5MB
- [ ] File format should be: PNG, JPG, JPEG, GIF, WebP

**Issue: "Upload failed"**
- [ ] Check backend terminal for error messages
- [ ] Check if backend server is running on port 5000
- [ ] Look for "Auth Header: None" in backend logs

**Issue: Images showing but not saving**
- [ ] Click "Save Changes" after uploading
- [ ] This saves the username and bio changes
- [ ] Images should be saved automatically after upload

## File Structure

```
uploads/
├── avatars/
│   ├── 20251203_130151_profile.jpg
│   └── ...
└── covers/
    ├── 20251203_130152_cover.jpg
    └── ...
```

## Key Files Modified

1. **Frontend**
   - `/client/src/components/ProfileCustomization.jsx` - Simplified upload UI
   - `/client/vite.config.js` - Added secure: false to proxy

2. **Backend**
   - `/server/middleware/auth.py` - Added debug logging
   - `/server/routes/user_routes.py` - Has upload endpoints

3. **Styling**
   - `/client/src/styles/profile.css` - Upload zone styles

## Testing Workflow

```
1. npm run dev                    # Start frontend on port 3000
2. python app.py                 # Start backend on port 5000 (in different terminal)
3. Open http://localhost:3000    # Open frontend
4. Sign up → Go to Profile → Edit Profile → Upload Images → Save
```

## Next Steps If Still Not Working

1. Open browser DevTools (F12)
2. Go to Network tab
3. Try uploading an image
4. Look for the POST request to `/api/users/profile/upload-avatar`
5. Check:
   - Request Headers - should have Authorization: Bearer {token}
   - Response Status - should be 200
   - Response Body - should have user object with avatar URL

6. Open backend terminal and look for:
   - "Auth Header: Bearer ..."
   - No error messages
