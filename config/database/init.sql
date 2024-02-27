CREATE ROLE minimal_user WITH LOGIN PASSWORD 'minimal_password';
GRANT USAGE ON SCHEMA public TO minimal_user;

CREATE ROLE admin_user WITH LOGIN PASSWORD 'admin_password';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;

CREATE TABLE IF NOT EXISTS "User" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    auth_id VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS "Group" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS "UserInGroup" (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "User" (id) ON DELETE CASCADE,
    group_id INT REFERENCES "Group" (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Message" (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    sender_id INT REFERENCES "User" (id) ON DELETE CASCADE,
    receiver_group_id INT REFERENCES "Group" (id) ON DELETE CASCADE,
    date_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Media" (
    id SERIAL PRIMARY KEY,
    type_ VARCHAR(50) NOT NULL,
    link VARCHAR(255) NOT NULL,
    message_id INT REFERENCES "Message" (id) ON DELETE CASCADE
);
