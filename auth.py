from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
import bcrypt
import uuid

def setup_auth(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  
    jwt = JWTManager(app)
    return jwt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash)