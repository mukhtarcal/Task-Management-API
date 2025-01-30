CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    dueDate DATETIME NOT NULL,
    status ENUM('pending', 'in-progress', 'completed') NOT NULL
);

