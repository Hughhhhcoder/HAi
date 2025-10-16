-- 为 psych_tests 表添加 ai_report 字段
-- 用于存储 AI 生成的专业评估报告

ALTER TABLE psych_tests ADD COLUMN ai_report TEXT NULL COMMENT 'AI 生成的专业评估报告';

