# Instagram-like Profile Photo Upload Feature

## Overview
Implemented a complete photo upload system for user profiles, allowing users to update their avatar and cover images with drag-and-drop functionality, real-time preview, and file validation.

## Changes Made

### Backend (Python Flask)

#### 1. **user_routes.py** - Added Image Upload Endpoints
- **New Imports**: Added `werkzeug.utils.secure_filename`, `os`, `datetime`, and `mimetypes`
- **Configuration Constants**:
  - `UPLOAD_FOLDER`: Path to store uploads
  - `ALLOWED_EXTENSIONS`: {'png', 'jpg', 'jpeg', 'gif', 'webp'}
  - `MAX_FILE_SIZE`: 5MB limit per file

- **Helper Functions**:
  - `allowed_file(filename)`: Validates file extension
  - `save_upload_file(file, subfolder)`: Saves file with validation and generates unique filenames

- **New API Endpoints**:
  - `POST /api/users/profile/upload-avatar`: Upload user avatar
  - `POST /api/users/profile/upload-cover`: Upload cover image
  - Both endpoints return updated user data

### Frontend (React)

#### 1. **ProfileCustomization.jsx** - Enhanced Photo Upload Component
- **New Features**:
  - File input fields for avatar and cover image
  - Real-time image preview
  - Drag-and-drop support for both images
  - Immediate upload on file selection
  - Loading state during upload
  - Error handling with user feedback
  - Visual feedback for drag-active state

- **Key Methods**:
  - `handleAvatarChange()` & `handleCoverChange()`: Handle file selection
  - `previewImage()`: Generate preview and trigger upload
  - `uploadImage()`: Async file upload with FormData
  - Drag event handlers for drag-and-drop functionality

#### 2. **Profile.jsx** - Updated Profile Page
- Added `handleImageUpload()` callback function
- Passes `onImageUpload` prop to `ProfileCustomization` component
- Updates local state when images are successfully uploaded

#### 3. **profile.css** - Comprehensive Styling
New CSS classes for:
- `.image-upload-zone`: Main upload area with dashed border
- `.drag-active`: Visual feedback during drag
- `.upload-placeholder`: Upload prompt styling
- `.image-preview`: Preview container for uploaded images
- `.avatar-preview` & `.cover-preview`: Specific preview dimensions
- `.overlay`: Hover effect with "Change" button
- `.change-btn`: Button styling for changing images
- Theme support (light and dark modes)
- Focus states and transitions

### Features

✅ **Image Upload**
- Drag-and-drop upload
- Click to select file
- Multiple file type support (PNG, JPG, JPEG, GIF, WebP)

✅ **Validation**
- File type validation
- 5MB file size limit
- Error messages displayed to user

✅ **User Experience**
- Real-time image preview
- Immediate upload on selection
- Loading state during upload
- Hover overlay with "Change" button
- Theme support (light/dark modes)
- Responsive design

✅ **File Management**
- Unique filename generation with timestamp
- Organized folder structure (avatars/, covers/)
- Secure filename handling

## File Structure

```
uploads/
├── avatars/
│   └── [timestamp]_[filename].jpg
└── covers/
    └── [timestamp]_[filename].jpg
```

## API Response

**Success Response (200)**
```json
{
  "message": "Avatar uploaded successfully",
  "user": {
    "id": 1,
    "username": "Arthi",
    "email": "arthi@example.com",
    "bio": "Bio text",
    "avatar": "/uploads/avatars/20231215_120530_profile.jpg",
    "coverImage": "/uploads/covers/20231215_120531_cover.jpg",
    "createdAt": "2023-12-15T10:00:00"
  }
}
```

**Error Response (400/500)**
```json
{
  "message": "File type not allowed. Use: PNG, JPG, JPEG, GIF, WebP"
}
```

## Installation/Setup

1. **Backend Dependencies**: No additional dependencies required (uses existing Flask, werkzeug)

2. **Frontend**: Already uses axios for HTTP requests

3. **Server Configuration**: Ensure uploads folder exists and is writable:
   ```bash
   mkdir -p server/uploads/{avatars,covers,posts}
   chmod 755 server/uploads
   ```

## Usage

1. Click "Edit Profile" button
2. For avatar:
   - Click the upload area OR drag-and-drop a file
   - See instant preview
   - Image uploads automatically
3. For cover image:
   - Same process as avatar
   - Larger preview area
4. Fill in other profile details (username, bio)
5. Click "Save Changes" to finalize profile update

## Theme Support

The UI automatically adapts to light and dark themes using CSS variables:
- `--card-light` / `--card-dark`
- `--border-light` / `--border-dark`

## Security Considerations

✓ File type validation (whitelist approach)
✓ File size limit (5MB)
✓ Secure filename handling
✓ JWT authentication required
✓ Unique filename with timestamp prevents overwrites

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- IE11: No support (uses File API and FormData)

## Future Enhancements

- [ ] Image compression before upload
- [ ] Crop/resize functionality
- [ ] Multiple photos gallery
- [ ] Image filters
- [ ] CDN integration for image storage
- [ ] WebP automatic conversion
- [ ] Progressive image loading
