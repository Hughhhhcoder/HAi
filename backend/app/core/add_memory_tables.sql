-- 用户长期记忆表
CREATE TABLE IF NOT EXISTS user_memories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    role_id INT DEFAULT NULL,
    memory_type VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,
    importance INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    access_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES ai_roles(id),
    INDEX idx_user_role (user_id, role_id),
    INDEX idx_memory_type (memory_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户深层洞察表
CREATE TABLE IF NOT EXISTS user_insights (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    core_traits TEXT,
    main_concerns TEXT,
    strengths TEXT,
    coping_patterns TEXT,
    triggers TEXT,
    summary TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

