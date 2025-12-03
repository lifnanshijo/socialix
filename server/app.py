from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.database import init_db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400  # 24 hours

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')

@app.route('/')
def home():
    return {'message': 'Social Connect API is running'}

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
