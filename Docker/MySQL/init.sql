
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    id serial PRIMARY KEY,
    name varchar(50) UNIQUE NOT NULL,
    email varchar(100) UNIQUE NOT NULL,
    password varchar(64) NOT NULL,
    login_count integer NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE channels (
    id serial PRIMARY KEY,
    users_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE,
    name varchar(20) UNIQUE NOT NULL,
    description varchar(50) NOT NULL,
    is_owner BOOLEAN NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    users_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (users_id) REFERENCES users(id) ON DELETE CASCADE,
    channel_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    content text,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);
