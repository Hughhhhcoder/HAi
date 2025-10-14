-- 添加专业心理学知识库表
CREATE TABLE IF NOT EXISTS psychology_knowledge (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '知识标题',
    category VARCHAR(100) NOT NULL COMMENT '分类：theory/technique/case/symptom/intervention',
    subcategory VARCHAR(100) COMMENT '子分类：如 CBT/psychodynamic/humanistic',
    content TEXT NOT NULL COMMENT '知识内容（详细描述）',
    keywords TEXT COMMENT '关键词，逗号分隔，用于检索',
    source VARCHAR(500) COMMENT '来源（文献、书籍等）',
    reliability_score INT DEFAULT 8 COMMENT '可靠性评分 1-10',
    usage_count INT DEFAULT 0 COMMENT '被使用次数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_title (title),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='心理学专业知识库';

-- 添加角色与知识的多对多关系表
CREATE TABLE IF NOT EXISTS role_knowledge_mapping (
    role_id INT NOT NULL COMMENT 'AI角色ID',
    knowledge_id INT NOT NULL COMMENT '知识ID',
    priority INT DEFAULT 5 COMMENT '该知识对该角色的重要性 1-10',
    PRIMARY KEY (role_id, knowledge_id),
    FOREIGN KEY (role_id) REFERENCES ai_roles(id) ON DELETE CASCADE,
    FOREIGN KEY (knowledge_id) REFERENCES psychology_knowledge(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色-知识关联表';

-- 添加知识使用日志表
CREATE TABLE IF NOT EXISTS knowledge_usage_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL COMMENT '对话ID',
    knowledge_id INT NOT NULL COMMENT '知识ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role_id INT NOT NULL COMMENT 'AI角色ID',
    relevance_score FLOAT COMMENT '检索时的相关性得分',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (knowledge_id) REFERENCES psychology_knowledge(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES ai_roles(id) ON DELETE CASCADE,
    INDEX idx_conversation (conversation_id),
    INDEX idx_knowledge (knowledge_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='知识使用日志';

