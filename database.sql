CREATE DATABASE IF NOT EXISTS nlp_recruitment;
USE nlp_recruitment;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    resume_id INT,
    status VARCHAR(40) DEFAULT 'Under Review',
    match_score DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL
);

INSERT INTO users (name, email, password, role)
VALUES ('Admin', 'admin@system.local', 'admin', 'admin')
ON DUPLICATE KEY UPDATE password = VALUES(password);

INSERT INTO jobs (title, description, location) VALUES
('NLP Engineer', 'Build text pipelines, entity extraction, and ranking models.', 'Remote'),
('Data Analyst', 'Work with dashboards, SQL, and ad-hoc analysis.', 'New York'),
('Full Stack Developer', 'Flask/React experience with RESTful APIs.', 'Remote');

INSERT INTO users (name, email, password, role)
VALUES ('Sample Candidate', 'candidate@example.com', 'password', 'user')
ON DUPLICATE KEY UPDATE password = VALUES(password);

INSERT INTO resumes (user_id, content)
SELECT id, 'Experienced NLP engineer skilled in Python, Flask, SQL, text processing, and ranking algorithms.'
FROM users WHERE email = 'candidate@example.com'
ON DUPLICATE KEY UPDATE content = VALUES(content);

INSERT INTO applications (user_id, job_id, resume_id, status, match_score)
SELECT u.id, j.id, r.id, 'Under Review', 68.00
FROM users u
JOIN jobs j ON j.title = 'NLP Engineer'
JOIN resumes r ON r.user_id = u.id
WHERE u.email = 'candidate@example.com'
LIMIT 1;

