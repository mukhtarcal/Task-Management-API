from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime, timedelta
import bcrypt

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app)

# Initialize JWT Manager
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a random secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Specify where to look for the token
app.config['JWT_HEADER_NAME'] = 'Authorization'  # Default is 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # Default is 'Bearer'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) # token expires after year
jwt = JWTManager(app)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409
        
        user_id = str(uuid.uuid4())
        password_hash = hash_password(data['password'])  # Hash the password
        cursor.execute(
            "INSERT INTO users (id, username, password_hash) VALUES (%s, %s, %s)",
            (user_id, data['username'], password_hash)
        )
        conn.commit()
        
        access_token = create_access_token(identity=user_id)
        return jsonify({'token': access_token}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        user = cursor.fetchone()
        
        if user and check_password(data['password'], user['password_hash']):
            access_token = create_access_token(identity=user['id'])
            return jsonify({'token': access_token})
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        cursor.close()
        conn.close()

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE user_id = %s;", (current_user,))
        tasks = cursor.fetchall()
        return jsonify(tasks)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks/<uuid:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s;", (str(task_id), current_user))
        task = cursor.fetchone()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    required_fields = ['title', 'dueDate', 'status']
    if not all(field in request.json for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if len(request.json['title']) > 100:
        return jsonify({'error': 'Title must be 100 characters or less'}), 400
        
    if request.json['status'] not in ['pending', 'in-progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400
    
    try:
        datetime.fromisoformat(request.json['dueDate'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO 8601 format'}), 400
    
    new_task = {
        'id': str(uuid.uuid4()),
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'dueDate': request.json['dueDate'],
        'status': request.json['status'],
        'user_id': get_jwt_identity()
    }
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (id, title, description, dueDate, status, user_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (new_task['id'], new_task['title'], new_task['description'],
              new_task['dueDate'], new_task['status'], new_task['user_id']))
        conn.commit()
        return jsonify(new_task), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks/<uuid:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
    if not request.json:
        return jsonify({'error': 'No update data provided'}), 400
        
    if 'title' in request.json and len(request.json['title']) > 100:
        return jsonify({'error': 'Title must be 100 characters or less'}), 400
        
    if 'status' in request.json and request.json['status'] not in ['pending', 'in-progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (str(task_id), current_user))
        task = cursor.fetchone()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
            
        updates = {
            'title': request.json.get('title', task['title']),
            'description': request.json.get('description', task['description']),
            'dueDate': request.json.get('dueDate', task['dueDate']),
            'status': request.json.get('status', task['status'])
        }
        
        cursor.execute("""
            UPDATE tasks 
            SET title = %s, description = %s, dueDate = %s, status = %s 
            WHERE id = %s AND user_id = %s;
        """, (updates['title'], updates['description'], updates['dueDate'],
              updates['status'], str(task_id), current_user))
        conn.commit()
        return jsonify({'id': str(task_id), **updates})
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks/<uuid:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s;", (str(task_id), current_user))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        conn.commit()
        return jsonify({'result': 'Task deleted'})
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)