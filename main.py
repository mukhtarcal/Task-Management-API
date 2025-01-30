from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

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

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks;")
        tasks = cursor.fetchall()
        return jsonify(tasks)
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks/<uuid:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE id = %s;", (str(task_id),))
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
        'status': request.json['status']
    }
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (id, title, description, dueDate, status)
            VALUES (%s, %s, %s, %s, %s);
        """, (new_task['id'], new_task['title'], new_task['description'],
              new_task['dueDate'], new_task['status']))
        conn.commit()
        return jsonify(new_task), 201
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks/<uuid:task_id>', methods=['PUT'])
def update_task(task_id):
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
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (str(task_id),))
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
            WHERE id = %s;
        """, (updates['title'], updates['description'], updates['dueDate'],
              updates['status'], str(task_id)))
        conn.commit()
        return jsonify({'id': str(task_id), **updates})
    except Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/tasks/<uuid:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s;", (str(task_id),))
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