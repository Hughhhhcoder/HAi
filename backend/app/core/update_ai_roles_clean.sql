-- 更新AI角色，添加用户可见的描述（清理版）
UPDATE ai_roles SET 
  description = '帮助您识别和改变消极思维模式，建立积极的认知方式。擅长处理焦虑、抑郁和压力管理问题。',
  emoji = '🧠',
  tags = '焦虑,抑郁,压力管理',
  gradient = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
WHERE id = 1;

UPDATE ai_roles SET 
  description = '引导您理解和管理情绪，提升情绪智力。专注于情绪调节、愤怒管理和情感表达。',
  emoji = '💝',
  tags = '情绪调节,愤怒管理,情感表达',
  gradient = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
WHERE id = 2;

UPDATE ai_roles SET 
  description = '通过正念冥想帮助您活在当下，减少焦虑和压力。教授正念技巧和放松方法。',
  emoji = '🧘',
  tags = '正念,冥想,放松',
  gradient = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
WHERE id = 3;

UPDATE ai_roles SET 
  description = '改善家庭沟通，化解家庭矛盾，促进和谐关系。专注于亲子关系和夫妻沟通。',
  emoji = '👨‍👩‍👧‍👦',
  tags = '亲子关系,夫妻沟通,家庭矛盾',
  gradient = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
WHERE id = 4;

UPDATE ai_roles SET 
  description = '应对职场压力，提升工作效能，实现职业发展。帮助处理工作倦怠和职业规划。',
  emoji = '💼',
  tags = '职场压力,工作倦怠,职业规划',
  gradient = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
WHERE id = 5;

UPDATE ai_roles SET 
  description = '专注青少年成长问题，帮助度过青春期困惑。处理学业压力、人际关系和自我认同。',
  emoji = '🎓',
  tags = '学业压力,人际关系,自我认同',
  gradient = 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)'
WHERE id = 6;

UPDATE ai_roles SET 
  description = '改善睡眠质量，解决失眠和睡眠障碍问题。提供作息调整和睡眠卫生指导。',
  emoji = '😴',
  tags = '失眠,睡眠质量,作息调整',
  gradient = 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
WHERE id = 7;

UPDATE ai_roles SET 
  description = '帮助您从创伤经历中恢复，重建心理健康。提供创伤后应激和情感疗愈支持。',
  emoji = '🌱',
  tags = '创伤后应激,心理创伤,情感疗愈',
  gradient = 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
WHERE id = 8;

UPDATE ai_roles SET 
  description = '提升社交技能，改善人际关系，建立健康界限。处理社交焦虑和人际冲突。',
  emoji = '🤝',
  tags = '社交焦虑,人际冲突,沟通技巧',
  gradient = 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
WHERE id = 9;

UPDATE ai_roles SET 
  description = '激发内在潜能，实现自我价值，追求个人成长。专注于自我探索和人生意义。',
  emoji = '🌟',
  tags = '自我探索,人生意义,个人成长',
  gradient = 'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)'
WHERE id = 10;
