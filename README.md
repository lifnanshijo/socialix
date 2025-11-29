# Social Connect - Social Media Application

A full-stack social media application with authentication, profile customization, and dual theme support.

## Features

✅ **Authentication**
- Login and Signup with email/password
- Google OAuth integration
- JWT-based authentication
- Protected routes

✅ **Profile Management**
- User profiles with customization
- Avatar and cover image support
- Bio and user details
- Profile editing

✅ **Dual Theme Support**
- Light theme
- Dark theme
- Theme persistence using localStorage
- Smooth theme transitions

✅ **Modern Tech Stack**
- **Frontend:** React 18 with Vite
- **Backend:** Python Flask
- **Database:** MySQL
- **Authentication:** JWT + Google OAuth

## Project Structure

```
social connect/
├── client/                 # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── context/       # React Context (Auth, Theme)
│   │   ├── pages/         # Page components
│   │   └── styles/        # CSS files
│   ├── package.json
│   └── vite.config.js
│
└── server/                # Python Backend
    ├── config/            # Database configuration
    ├── middleware/        # Auth middleware
    ├── models/            # Database models
    ├── routes/            # API routes
    ├── app.py            # Main Flask application
    └── requirements.txt
```

## Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.8+)
- MySQL Server

### Backend Setup

1. Navigate to the server directory:
   ```powershell
   cd server
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

5. Create a `.env` file (copy from `.env.example`):
   ```powershell
   cp .env.example .env
   ```

6. Update `.env` with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=social_connect
   JWT_SECRET_KEY=your-secret-key-here
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   ```

7. Create the MySQL database:
   ```sql
   CREATE DATABASE social_connect;
   ```
   
   Or run the schema file:
   ```powershell
   mysql -u root -p < config/schema.sql
   ```

8. Run the Flask server:
   ```powershell
   python app.py
   ```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Open a new terminal and navigate to the client directory:
   ```powershell
   cd client
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Create a `.env` file (copy from `.env.example`):
   ```powershell
   cp .env.example .env
   ```

4. Update `.env` with your Google Client ID:
   ```
   VITE_API_URL=http://localhost:5000
   VITE_GOOGLE_CLIENT_ID=your-google-client-id
   ```

5. Run the development server:
   ```powershell
   npm run dev
   ```

The frontend will run on `http://localhost:3000`

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized JavaScript origins:
   - `http://localhost:3000`
6. Add authorized redirect URIs:
   - `http://localhost:3000`
7. Copy the Client ID and add it to both `.env` files

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/google` - Google OAuth login
- `GET /api/auth/me` - Get current user (protected)

### Users
- `GET /api/users/profile` - Get user profile (protected)
- `PUT /api/users/profile` - Update user profile (protected)
- `GET /api/users/:id` - Get user by ID
- `GET /api/users/search?q=username` - Search users

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `password` - Hashed password (null for OAuth users)
- `bio` - User bio
- `avatar` - Avatar URL
- `cover_image` - Cover image URL
- `oauth_provider` - OAuth provider (google, etc.)
- `oauth_id` - OAuth user ID
- `created_at` - Timestamp
- `updated_at` - Timestamp

## Features to Add

- [ ] Posts and feed
- [ ] Likes and comments
- [ ] Friend/follow system
- [ ] Real-time notifications
- [ ] Image upload functionality
- [ ] Message system
- [ ] User search and discovery

## Technologies Used

- **React** - UI library
- **React Router** - Client-side routing
- **Vite** - Build tool
- **Flask** - Python web framework
- **MySQL** - Relational database
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing
- **Google OAuth** - Social login

## License

MIT

## Contributing

Feel free to submit issues and pull requests!
