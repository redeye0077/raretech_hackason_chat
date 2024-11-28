
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) UNIQUE NOT NULL,
    email varchar(100) UNIQUE NOT NULL,
    password varchar(64) NOT NULL,
    login_count INT NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    name varchar(15) UNIQUE NOT NULL,
    description varchar(50) NOT NULL,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    channel_id INT NOT NULL,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    content text,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp on update current_timestamp
);

INSERT INTO users(id, name, email, password, login_count)VALUES(1,'テスト','test1@gmail.com','aaaa', 1);
INSERT INTO users(id, name, email, password, login_count)VALUES(2,'テ','test2@gmail.com','aaaa', 1);
INSERT INTO channels(id, user_id, name, description)VALUES(1, 1,'ぼっち部屋','テストさんの孤独な部屋です');
INSERT INTO channels(id, user_id, name, description)VALUES(2, 1,'ぼっち','テストさん');
INSERT INTO messages(id, user_id, channel_id, content, created_at)VALUES(1, 1, 1, '誰かかまってください、、', '2024-11-11 11:11:00');
INSERT INTO messages(id, user_id, channel_id, content, created_at)VALUES(2, 2, 1, 'アーニャ', '2024-10-10 10:10:00');
