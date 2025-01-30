# Task Management API

## Overview

This project is a backend API for managing tasks with CRUD operations. It is built using Flask and MySQL, and it is containerized using Docker and Docker Compose. The API includes user authentication using JWT (JSON Web Tokens) to secure task management operations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the API](#running-the-api)
- [User Authentication](#user-authentication)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)

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
   Go to the location where you would like this code folder to be and run the code below:
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
   DB_HOST=db
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

## User Authentication

### Register a New User (You can see clearly how to do later using cURL or Postman)

To register a new user, send a POST request to the `/auth/register` endpoint with the following JSON body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

### Login

To log in, send a POST request to the `/auth/login` endpoint with the following JSON body (You can see clearly how to do later using cURL or Postman):

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

On successful login, you will receive a JWT token in the response. Use this token for subsequent requests to protected endpoints.

### Using the JWT Token (tokens expire after 1 hour - re-login to attain new token)

Include the JWT token in the `Authorization` header for requests to protected endpoints (e.g., task management endpoints):

```
Authorization: Bearer <your_jwt_token>
```

## API Endpoints

- `POST /auth/register`: Register a new user.
- `POST /auth/login`: Log in and receive a JWT token.
- `GET /tasks`: Retrieve all tasks (requires authentication).
- `POST /tasks`: Create a new task (requires authentication).
- `GET /tasks/{id}`: Retrieve a task by ID (requires authentication).
- `PUT /tasks/{id}`: Update a task by ID (requires authentication).
- `DELETE /tasks/{id}`: Delete a task by ID (requires authentication).

## Testing the API

You can test the API using tools like Postman, cURL, or your web browser. Below are examples of how to test the API endpoints. Make sure the backend is running first.

### Using cURL (recommended)

1. **Register a New User**:
   ```bash
   curl -X POST http://localhost:5001/auth/register -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
   ```

2. **Login**:
   ```bash
   curl -X POST http://localhost:5001/auth/login -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}'
   ```

   Example token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczODIxODMxNiwianRpIjoiZDA4OWEwMDMtZjVmOC00ODhkLTkwZDAtMTBiOTBjNjc4N2YwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjA5ZjdlMjI0LWM3NzctNDBkNy1iNjkyLTkyNzM2ZmVkMjdmNSIsIm5iZiI6MTczODIxODMxNiwiZXhwIjoxNzY5NzU0MzE2fQ.oNUkFVPwhcVgSFVJwqx4ELRXBwPNV9-86diHKq4g8OY"

3. **Get All Tasks** (after obtaining the JWT token):
   ```bash
   curl -X GET http://localhost:5001/tasks -H "Authorization: Bearer <your_jwt_token>"
   ```

4. **Create a New Task** (after obtaining the JWT token):
   ```bash
   curl -X POST http://localhost:5001/tasks -H "Content-Type: application/json" -H "Authorization: Bearer <your_jwt_token>" -d '{"title": "Test Task", "description": "This is a test task", "dueDate": "2023-12-31T00:00:00", "status": "pending"}'
   ```

5. **Update a Task** (after obtaining the JWT token):
   ```bash
   curl -X PUT http://localhost:5001/tasks/<task_id> -H "Content-Type: application/json" -H "Authorization: Bearer <your_jwt_token>" -d '{"title": "Updated Task", "status": "completed"}'
   ```

6. **Delete a Task** (after obtaining the JWT token):
   ```bash
   curl -X DELETE http://localhost:5001/tasks/<task_id> -H "Authorization: Bearer <your_jwt_token>"
   ```

### Using Postman

1. **Register a New User**: Set the request type to POST and enter the URL `http://localhost:5001/auth/register`. In the "Body" tab, select "raw" and set the type to "JSON". Enter the JSON data for the user.

2. **Login**: Set the request type to POST and enter the URL `http://localhost:5001/auth/login`. In the "Body" tab, select "raw" and set the type to "JSON". Enter the JSON data for the user.

3. **Get All Tasks**: Set the request type to GET and enter the URL `http://localhost:5001/tasks`. In the "Headers" tab, add a new header with the key `Authorization` and the value `Bearer <your_jwt_token>`.

4. **Create a New Task**: Set the request type to POST and enter the URL `http://localhost:5001/tasks`. In the "Body" tab, select "raw" and set the type to "JSON". Enter the JSON data for the task, and add the `Authorization` header as described above.

5. **Update a Task**: Set the request type to PUT and enter the URL `http://localhost:5001/tasks/<task_id>`. In the "Body" tab, select "raw" and set the type to "JSON". Enter the JSON data for the updated task, and add the `Authorization` header as described above.

6. **Delete a Task**: Set the request type to DELETE and enter the URL `http://localhost:5001/tasks/<task_id>`. In the "Headers" tab, add a new header with the key `Authorization` and the value `Bearer <your_jwt_token>`.

## API Endpoints

- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Create a new task.
- `GET /tasks/{id}`: Retrieve a task by ID.
- `PUT /tasks/{id}`: Update a task by ID.
- `DELETE /tasks/{id}`: Delete a task by ID.

## Conclusion

This README provides a comprehensive guide to setting up and using the Task Management API. Follow the instructions carefully to ensure a smooth experience. If you encounter any issues, please refer to the documentation for troubleshooting tips or reach out for support.