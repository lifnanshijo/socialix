from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.database import init_db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.post_routes import post_bp
from routes.chat_routes import chat_bp
from routes.follow_routes import follow_bp
from routes.clip_routes import clips_bp
from utils.clips_scheduler import ClipsScheduler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max request size

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(post_bp, url_prefix='/api/posts')
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_blueprint(follow_bp, url_prefix='/api/users')
app.register_blueprint(clips_bp, url_prefix='/api/clips')

@app.route('/')
def home():
    return {'message': 'Social Connect API is running'}

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    scheduler = ClipsScheduler()
    scheduler.init_scheduler(app)
    app.run(debug=True, port=5000)
