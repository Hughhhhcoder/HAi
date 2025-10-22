-- 添加 email 字段到 users 表
ALTER TABLE users ADD COLUMN email VARCHAR(128) UNIQUE NULL COMMENT '用户邮箱';
ALTER TABLE users ADD INDEX idx_email (email);

