# Task Management API

## Overview

This project is a backend API for managing tasks with CRUD operations. It is built using Flask and MySQL, and it is containerized using Docker and Docker Compose.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the API](#running-the-api)
- [Testing the API](#testing-the-api)
- [API Endpoints](#api-endpoints)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **[Docker](https://www.docker.com/get-started)**: Used to run the application in containers.
  - **Verify Installation**: Run the following command in your terminal:
    ```bash
    docker --version
    ```
  
- **[Docker Compose](https://docs.docker.com/compose/install/)**: Used to define and run multi-container Docker applications.
  - **Verify Installation**: Run the following command in your terminal:
    ```bash
    docker-compose --version
    ```

- **[Git](https://git-scm.com/downloads)** (optional, for cloning the repository): Version control system to manage your code.
  - **Verify Installation**: Run the following command in your terminal:
    ```bash
    git --version
    ```

- **[Python](https://www.python.org/downloads/)**: Required for running the backend application.
  - **Verify Installation**: Run the following command in your terminal:
    ```bash
    python --version
    ```
    or for Python 3 specifically:
    ```bash
    python3 --version
    ```

- **[pip](https://pip.pypa.io/en/stable/)**: Python package installer, used to install dependencies.
  - **Verify Installation**: Run the following command in your terminal:
    ```bash
    pip --version
    ```
    or for pip3 specifically:
    ```bash
    pip3 --version
    ```

Make sure all the above tools are installed and accessible from your command line before proceeding with the setup instructions.

## Setup Instructions

1. **Clone the Repository**:
    Go to location where you would like this code folder to be and run the code below:
   ```bash
   git clone https://github.com/yourusername/Task-Management-API.git
   cd Task-Management-API
   ```

2. **Create a `.env` File**:
   Create a `.env` file in the root of the project directory with the following content:
   ```plaintext
   DB_USER=task_user
   DB_PASSWORD=task_password
   DB_NAME=task_db
   ```

3. **Build and Start the Containers**:
   Run the following command to build the Docker images and start the containers:
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the API service and the MySQL database service.
   - Initialize the database with the provided SQL script.

4. **Access the API**:
   The API will be running at `http://localhost:5001`.

## Running the API

To run the API, ensure that the Docker containers are up and running. You can check the logs to confirm that the API is running without errors:

To check the logs to confirm that the API is running without errors, in a new terminal, run:

```bash
docker-compose logs -f
```

To stop the containers, press `CTRL+C` in the terminal where the containers are running, or, in a new terminal, run:

```bash
docker-compose down
```

## Testing the API

You can test the API using tools like Postman, cURL, or your web browser. Below are examples of how to test the API endpoints. 

### Using cURL (Easiest)

1. **Get All Tasks**:
   ```bash
   curl -X GET http://localhost:5001/tasks
   ```

2. **Create a New Task**:
   ```bash
   curl -X POST http://localhost:5001/tasks -H "Content-Type: application/json" -d '{"title": "Test Task", "description": "This is a test task", "dueDate": "2023-12-31T00:00:00", "status": "pending"}'
   ```

3. **Get a Task by ID**:
   Replace `<task_id>` with the actual ID of the task you created.
   ```bash
   curl -X GET http://localhost:5001/tasks/<task_id>
   ```

4. **Update a Task**:
   Replace `<task_id>` with the actual ID of the task you want to update.
   ```bash
   curl -X PUT http://localhost:5001/tasks/<task_id> -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "Updated description", "dueDate": "2023-12-31T00:00:00", "status": "in-progress"}'
   ```

5. **Delete a Task**:
   Replace `<task_id>` with the actual ID of the task you want to delete.
   ```bash
   curl -X DELETE http://localhost:5001/tasks/<task_id>
   ```

### Using Postman

1. Open Postman and create a new request.
2. Set the request type (GET, POST, PUT, DELETE) based on the operation you want to perform.
3. Enter the URL (e.g., `http://localhost:5001/tasks`).
4. For POST and PUT requests, go to the "Body" tab, select "raw", and set the type to "JSON". Enter the JSON data for the task.
5. Click "Send" to execute the request and view the response.


### Using a Web Browser

You can test the GET endpoints directly in your web browser (Chrome, Firefox, Safari, etc.):

View All Tasks:

Open your web browser
Navigate to: http://localhost:5001/tasks
You should see a JSON response with all tasks, or an empty array [] if no tasks exist


View Single Task:

Navigate to: http://localhost:5001/tasks/<task_id>
Replace <task_id> with an actual task ID
You should see the JSON data for that specific task

Note: Browser testing is limited to GET requests only. For POST, PUT, and DELETE operations, please use cURL or Postman as described above.



## API Endpoints

- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Create a new task.
- `GET /tasks/{id}`: Retrieve a task by ID.
- `PUT /tasks/{id}`: Update a task by ID.
- `DELETE /tasks/{id}`: Delete a task by ID.

