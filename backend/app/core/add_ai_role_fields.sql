-- 为 ai_roles 表添加用户可见字段
ALTER TABLE ai_roles 
ADD COLUMN description TEXT NULL COMMENT '用户可见的角色描述',
ADD COLUMN emoji VARCHAR(20) NULL COMMENT '角色图标',
ADD COLUMN tags VARCHAR(255) NULL COMMENT '标签，逗号分隔',
ADD COLUMN gradient VARCHAR(200) NULL COMMENT '渐变色彩';
