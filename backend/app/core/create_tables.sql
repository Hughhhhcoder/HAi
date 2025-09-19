-- 按照外键依赖关系，先删除子表
DROP TABLE IF EXISTS literature_chunks;
DROP TABLE IF EXISTS literature_files;
DROP TABLE IF EXISTS psych_tests;
DROP TABLE IF EXISTS recovery_plans;
DROP TABLE IF EXISTS user_profiles;
DROP TABLE IF EXISTS daily_checkin;
DROP TABLE IF EXISTS rewards;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS ai_roles;
DROP TABLE IF EXISTS users;

-- 创建用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(32) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建AI角色表
CREATE TABLE ai_roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(32) NOT NULL UNIQUE,
    prompt_template VARCHAR(1024) NOT NULL,
    INDEX idx_role_name (role_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建对话历史表
CREATE TABLE conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    message TEXT NOT NULL,
    is_user BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(256),
    audio_url VARCHAR(256),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES ai_roles(id),
    INDEX idx_user_role (user_id, role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建用户作息表
CREATE TABLE user_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    sleep_time VARCHAR(8),
    wake_time VARCHAR(8),
    preferences VARCHAR(256),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建生活恢复计划表
CREATE TABLE recovery_plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    plan_text TEXT NOT NULL,
    stage VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建心理测评表
CREATE TABLE psych_tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    test_type VARCHAR(32) NOT NULL,
    answers_json TEXT NOT NULL,
    score INT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建每日打卡表
CREATE TABLE daily_checkin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    mood VARCHAR(32),
    sleep_hours FLOAT,
    completed_tasks VARCHAR(256),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建积分与奖励表
CREATE TABLE rewards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    points INT NOT NULL DEFAULT 0,
    reward_history VARCHAR(256),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建文献元数据表
CREATE TABLE literature_files (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(128) NOT NULL,
    file_path VARCHAR(256) NOT NULL,
    file_type VARCHAR(16) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建文献分段内容表
CREATE TABLE literature_chunks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    chunk_index INT NOT NULL,
    text TEXT NOT NULL,
    embedding VARCHAR(1024),
    FOREIGN KEY (file_id) REFERENCES literature_files(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 