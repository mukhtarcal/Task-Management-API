from flask import Flask, jsonify, request
import mysql.connector
import os
import uuid

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks;")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks)

# get task by id
@app.route('/tasks/<uuid:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(task)

# create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    new_task = {
        'id': str(uuid.uuid4()),
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'dueDate': request.json['dueDate'],
        'status': request.json['status']
    }
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (id, title, description, dueDate, status) VALUES (%s, %s, %s, %s, %s);",
                   (new_task['id'], new_task['title'], new_task['description'], new_task['dueDate'], new_task['status']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_task), 201

# update a task
@app.route('/tasks/<uuid:task_id>', methods=['PUT'])
def update_task(task_id):
    updates = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = %s, description = %s, dueDate = %s, status = %s WHERE id = %s;",
                   (updates['title'], updates.get('description', ''), updates['dueDate'], updates['status'], task_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'id': task_id, **updates})

# remove a task
@app.route('/tasks/<uuid:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'result': 'Task deleted'})