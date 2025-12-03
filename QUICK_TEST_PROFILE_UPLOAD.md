# Quick Start - Profile Image Upload Testing

## 🚀 Current Status
✅ Backend: Running on http://localhost:5000
✅ Frontend: Running on http://localhost:3001
✅ Database: MySQL with BLOB storage configured
✅ API: All endpoints working

## 📋 Testing Checklist

### Setup (Already Done ✅)
- [x] Backend server running
- [x] Frontend server running
- [x] Database created with BLOB schema
- [x] ProfileCustomization component fixed
- [x] AuthContext configured with API URL
- [x] Profile component updated

### Test Flow

#### 1️⃣ Login to Application
- Visit: http://localhost:3001
- If not logged in, sign up or login with test account:
  - Email: `blobtest@example.com`
  - Password: `TestPass123!`

#### 2️⃣ Navigate to Profile
- Click profile icon/avatar in navbar
- Should see profile page with current images

#### 3️⃣ Click "Edit Profile"
- "Edit Profile" button appears in top right
- Form should expand below profile header
- Shows upload zones for:
  - Profile Picture
  - Cover Image

#### 4️⃣ Upload Avatar Image
- Click on "Profile Picture" upload area
- Select an image file (JPG, PNG, GIF, WebP)
- Image should show as preview immediately
- **Important**: Don't click "Save Changes" yet - preview should work first

#### 5️⃣ Upload Cover Image (Optional)
- Click on "Cover Image" upload area
- Select a larger image for cover
- Image shows as preview

#### 6️⃣ Update Profile Fields (Optional)
- Optionally change username
- Optionally update bio text

#### 7️⃣ Click "Save Changes"
- Should show "Saving..." state
- Should get success alert: "Profile updated successfully!"
- Profile page should refresh with new images

#### 8️⃣ Verify Images Persist
- Refresh page (F5)
- Navigate away and back to profile
- Images should still be there
- This confirms BLOB storage working!

## 🐛 Expected Behavior

### What Should Happen ✅
```
1. Image preview appears immediately when selected
2. All fields can be edited (images + text)
3. Click Save Changes
4. Success message appears
5. Page updates with new data
6. Images persist after refresh
7. No network errors
8. No database errors
```

### If Something Goes Wrong ❌

#### Error: "Network Error" / "localhost:3000"
```
Cause: Browser hasn't refreshed yet
Fix: Hard refresh Ctrl+F5 in browser
```

#### Error: "Profile update failed"
```
Check:
1. Backend console for errors
2. Browser console (F12) for errors
3. Network tab for 401/500 errors
4. Verify token is present
```

#### Images upload but don't save
```
Fix: Make sure to click "Save Changes" button
```

#### Images show but disappear after refresh
```
Possible causes:
1. Database not saving properly
2. BLOB columns not created
3. Check MySQL database directly

Test:
```sql
SELECT id, username, avatar_type FROM users;
```
```

#### 401 Unauthorized
```
Cause: JWT token expired or missing
Fix: 
1. Logout (clear localStorage)
2. Login again
3. Try upload again
```

## 🔍 Manual Database Verification

Open MySQL and run:

```sql
-- Check users table structure
DESCRIBE users;

-- You should see:
-- avatar | LONGBLOB
-- avatar_type | VARCHAR(50)
-- cover_image | LONGBLOB
-- cover_image_type | VARCHAR(50)

-- Check if avatar data is stored
SELECT id, username, LENGTH(avatar) as avatar_size, avatar_type 
FROM users 
WHERE avatar IS NOT NULL;

-- Should show avatar size in bytes (e.g., 50234)
```

## 📊 Debug Checklist

If upload isn't working, check in this order:

- [ ] Backend running: `curl http://localhost:5000/health`
- [ ] Frontend running: Visit http://localhost:3001
- [ ] Logged in: Check localStorage for 'token'
- [ ] Network tab (F12) shows PUT to http://localhost:5000/api/users/profile
- [ ] Response status is 200 (not 401, 400, 500)
- [ ] Response contains avatar as `data:image/...;base64,...`
- [ ] Browser console has no errors
- [ ] MySQL shows avatar data stored as LONGBLOB

## 📝 Test Scenarios

### Scenario 1: New Avatar Only
```
1. Click Edit Profile
2. Select avatar image
3. Leave cover image empty
4. Leave username/bio unchanged
5. Click Save
✓ Avatar should save, cover should stay as-is
```

### Scenario 2: Everything Changed
```
1. Click Edit Profile
2. Select avatar
3. Select cover image
4. Change username
5. Change bio
6. Click Save
✓ All fields should update
```

### Scenario 3: Text Only Change
```
1. Click Edit Profile
2. Don't select any images
3. Change username
4. Change bio
5. Click Save
✓ Only text should update, images unchanged
```

### Scenario 4: Persistence Test
```
1. Upload avatar
2. Click Save
3. Refresh page (F5)
4. Navigate to another page
5. Come back to profile
✓ Avatar should still be there
```

## 🔐 Security Check

Images should be stored as BLOB in database, not as file paths:

```bash
# Good ✅
Avatar in response: "data:image/jpeg;base64,/9j/4AAQSkZJRg..."

# Bad ❌
Avatar in response: "/uploads/user1_avatar.jpg"
```

## 📞 If Issues Persist

Check these files:
1. `client/src/context/AuthContext.jsx` - API_URL should be `http://localhost:5000`
2. `client/src/components/ProfileCustomization.jsx` - Uses correct API endpoint
3. `server/routes/user_routes.py` - PUT /api/users/profile endpoint
4. `server/config/database.py` - Users table has LONGBLOB columns

## ✅ Success Criteria

You'll know it's working when:

1. ✅ Can select image and see preview
2. ✅ Can click "Save Changes" without error
3. ✅ Success alert appears
4. ✅ Profile page updates with new image
5. ✅ Image persists after page refresh
6. ✅ No 401/404/500 errors in console
7. ✅ Database shows avatar as LONGBLOB bytes, not file path

---

**Ready?** Go test the profile upload now! 🎉
