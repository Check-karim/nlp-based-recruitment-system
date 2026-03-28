CREATE DATABASE IF NOT EXISTS nlp_recruitment;
USE nlp_recruitment;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
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
    filename VARCHAR(255),
    content TEXT NOT NULL,
    skills TEXT,
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

INSERT INTO users (name, username, email, password, role)
VALUES ('Admin', 'admin', 'admin@system.local', 'admin', 'admin')
ON DUPLICATE KEY UPDATE password = VALUES(password);

INSERT INTO jobs (title, description, location) VALUES
('NLP Engineer', 'Build text pipelines, entity extraction, and ranking models. Required skills: Python, NLP, machine learning, TensorFlow, data analysis.', 'Remote'),
('Data Analyst', 'Work with dashboards, SQL, and ad-hoc analysis. Required skills: SQL, Excel, Power BI, statistics, data analysis, Python.', 'New York'),
('Full Stack Developer', 'Flask/React experience with RESTful APIs. Required skills: Python, Flask, React, JavaScript, HTML, CSS, REST, Git.', 'Remote');

INSERT INTO users (name, username, email, password, role)
VALUES ('Sample Candidate', 'candidate', 'candidate@example.com', 'password', 'user')
ON DUPLICATE KEY UPDATE password = VALUES(password);

INSERT INTO resumes (user_id, filename, content, skills)
SELECT id, NULL,
    'Experienced NLP engineer skilled in Python, Flask, SQL, text processing, machine learning, and ranking algorithms. Proficient with TensorFlow, pandas, and data analysis.',
    'python, flask, sql, machine learning, tensorflow, pandas, data analysis, nlp'
FROM users WHERE email = 'candidate@example.com'
ON DUPLICATE KEY UPDATE content = VALUES(content);

INSERT INTO applications (user_id, job_id, resume_id, status, match_score)
SELECT u.id, j.id, r.id, 'Under Review', 68.00
FROM users u
JOIN jobs j ON j.title = 'NLP Engineer'
JOIN resumes r ON r.user_id = u.id
WHERE u.email = 'candidate@example.com'
LIMIT 1;
