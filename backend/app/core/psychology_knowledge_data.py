"""
预置的专业心理学知识数据
涵盖各种心理学理论、技术、症状、干预方法等
"""

PSYCHOLOGY_KNOWLEDGE_DATA = [
    # ========== 认知行为疗法 (CBT) ==========
    {
        "title": "认知行为疗法（CBT）核心原理",
        "category": "theory",
        "subcategory": "CBT",
        "content": """认知行为疗法认为，个体的情绪和行为问题源于不合理的认知模式。通过识别和挑战消极自动思维、核心信念，可以改善情绪困扰。核心技术包括：认知重构、行为激活、暴露疗法、问题解决训练等。CBT 强调此时此地，注重结构化和目标导向，通常为短程治疗（12-20次）。""",
        "keywords": "CBT,认知行为疗法,认知重构,自动思维,核心信念,焦虑,抑郁",
        "source": "Beck, A. T. (1976). Cognitive Therapy and the Emotional Disorders.",
        "reliability_score": 10
    },
    {
        "title": "认知扭曲的常见类型",
        "category": "technique",
        "subcategory": "CBT",
        "content": """常见认知扭曲包括：1) 全或无思维（黑白思维）；2) 过度概括化；3) 心理过滤（只看消极面）；4) 否定积极面；5) 妄下结论（读心术、算命式思维）；6) 放大与缩小；7) 情绪化推理；8) 应该式思维；9) 贴标签；10) 个人化。识别这些扭曲是认知重构的第一步。""",
        "keywords": "认知扭曲,黑白思维,过度概括,负面思维,认知重构",
        "source": "Burns, D. D. (1980). Feeling Good: The New Mood Therapy.",
        "reliability_score": 9
    },
    {
        "title": "行为激活治疗抑郁",
        "category": "intervention",
        "subcategory": "CBT",
        "content": """行为激活是治疗抑郁的有效方法。抑郁时，人们往往回避活动，导致愉悦感和成就感下降，形成恶性循环。行为激活鼓励患者：1) 监测日常活动和心情；2) 识别价值观和目标；3) 逐步增加有意义的活动；4) 减少回避行为。即使心情不好，也要先行动起来，情绪会随之改善。""",
        "keywords": "行为激活,抑郁,回避,活动安排,愉悦感,成就感",
        "source": "Martell, C. R., et al. (2001). Behavioral Activation for Depression.",
        "reliability_score": 9
    },
    
    # ========== 正念与接纳 ==========
    {
        "title": "正念减压（MBSR）基本原理",
        "category": "theory",
        "subcategory": "Mindfulness",
        "content": """正念减压（MBSR）由卡巴金创立，核心是培养对当下的非评判性觉察。通过正念呼吸、身体扫描、正念行走等练习，帮助个体从自动化反应模式中解脱，减轻压力、焦虑和慢性疼痛。正念强调接纳而非改变，通过觉察来与痛苦共处，提升内心平静和心理弹性。""",
        "keywords": "正念,MBSR,觉察,接纳,减压,焦虑,压力管理",
        "source": "Kabat-Zinn, J. (1990). Full Catastrophe Living.",
        "reliability_score": 10
    },
    {
        "title": "正念呼吸练习",
        "category": "technique",
        "subcategory": "Mindfulness",
        "content": """正念呼吸是最基础的正念练习。步骤：1) 找一个舒适的坐姿；2) 将注意力放在呼吸上（鼻孔、胸腔或腹部）；3) 当注意力飘走时，温柔地将它带回呼吸；4) 不评判自己的走神，这是自然现象。每天5-10分钟即可见效，有助于平静情绪、提升专注力。""",
        "keywords": "正念呼吸,冥想,放松,焦虑缓解,专注力",
        "source": "Kabat-Zinn, J. (1994). Wherever You Go, There You Are.",
        "reliability_score": 9
    },
    {
        "title": "接纳承诺疗法（ACT）核心",
        "category": "theory",
        "subcategory": "ACT",
        "content": """接纳承诺疗法（ACT）强调心理灵活性，包括六个核心过程：1) 接纳（允许不愉快的想法和感受存在）；2) 认知解离（不被想法主宰）；3) 活在当下；4) 观察者自我（从更大视角看待自己）；5) 价值澄清；6) 承诺行动（朝着价值方向行动）。ACT 不追求消除痛苦，而是帮助人们带着痛苦过有意义的生活。""",
        "keywords": "ACT,接纳承诺疗法,心理灵活性,价值观,接纳,认知解离",
        "source": "Hayes, S. C., et al. (1999). Acceptance and Commitment Therapy.",
        "reliability_score": 9
    },
    
    # ========== 积极心理学 ==========
    {
        "title": "PERMA 幸福模型",
        "category": "theory",
        "subcategory": "Positive Psychology",
        "content": """积极心理学家塞利格曼提出 PERMA 模型，认为幸福由五要素构成：1) Positive Emotion（积极情绪）：愉悦、感激、希望等；2) Engagement（投入）：心流体验；3) Relationships（关系）：良好的人际关系；4) Meaning（意义）：归属于并服务于比自己更大的东西；5) Achievement（成就）：追求目标和成功。培养这五方面可提升整体幸福感。""",
        "keywords": "PERMA,幸福,积极心理学,心流,意义,成就,关系",
        "source": "Seligman, M. E. P. (2011). Flourish.",
        "reliability_score": 10
    },
    {
        "title": "性格优势识别",
        "category": "technique",
        "subcategory": "Positive Psychology",
        "content": """积极心理学强调识别和运用个人优势。VIA（价值观行动）性格优势问卷识别 24 种性格优势，如创造力、勇敢、善良、感恩等。研究表明，运用自己的核心优势（top 5）可显著提升幸福感和工作满意度。引导来访者每天以新方式使用一项优势，可促进积极改变。""",
        "keywords": "性格优势,VIA,积极心理学,优势运用,幸福感",
        "source": "Peterson, C., & Seligman, M. E. P. (2004). Character Strengths and Virtues.",
        "reliability_score": 9
    },
    {
        "title": "感恩练习",
        "category": "intervention",
        "subcategory": "Positive Psychology",
        "content": """感恩练习是提升幸福感的简单有效方法。常见做法：每天睡前写下三件值得感恩的事，并思考为什么发生这些事。研究表明，坚持2-4周可显著提升积极情绪、减少抑郁。感恩帮助人们关注生活中的积极面，打破负面思维循环。""",
        "keywords": "感恩,感恩日记,幸福感,积极情绪,抑郁缓解",
        "source": "Emmons, R. A., & McCullough, M. E. (2003). Journal of Personality and Social Psychology.",
        "reliability_score": 9
    },
    
    # ========== 情绪聚焦疗法 (EFT) ==========
    {
        "title": "情绪聚焦疗法（EFT）核心理念",
        "category": "theory",
        "subcategory": "EFT",
        "content": """情绪聚焦疗法认为，情绪是适应性信息，而非需要消除的敌人。核心任务是帮助来访者：1) 觉察情绪（识别和命名情绪）；2) 体验情绪（允许情绪在身体中展开）；3) 表达情绪（用语言描述情绪体验）；4) 转化情绪（将不适应性情绪转化为适应性情绪）。EFT 特别强调识别"核心情绪"（如悲伤、恐惧、愤怒）和"次级情绪"（如焦虑、羞愧）。""",
        "keywords": "EFT,情绪聚焦疗法,情绪觉察,情绪体验,情绪表达,核心情绪",
        "source": "Greenberg, L. S. (2015). Emotion-Focused Therapy.",
        "reliability_score": 9
    },
    {
        "title": "空椅子技术",
        "category": "technique",
        "subcategory": "EFT",
        "content": """空椅子技术是格式塔疗法和 EFT 常用技术。来访者想象某个重要他人（或自己的某部分）坐在对面空椅子上，与之对话。这可以帮助：1) 表达未表达的情绪；2) 解决内在冲突（如批评自我 vs 脆弱自我）；3) 完成未完成的情绪事件。通过角色互换，来访者可以从不同视角理解问题。""",
        "keywords": "空椅子,格式塔疗法,情绪表达,内在对话,未完成事件",
        "source": "Perls, F. (1969). Gestalt Therapy Verbatim.",
        "reliability_score": 8
    },
    
    # ========== 创伤与 PTSD ==========
    {
        "title": "创伤知情护理原则",
        "category": "theory",
        "subcategory": "Trauma",
        "content": """创伤知情护理（Trauma-Informed Care）基于以下原则：1) 安全（物理和情绪上的安全）；2) 信任与透明；3) 同伴支持；4) 合作与互助；5) 赋权、发声与选择；6) 文化、历史与性别议题敏感。重要的是理解创伤对身心的影响，不问"你怎么了？"而问"你经历了什么？"避免二次创伤，强调当下的安全和稳定。""",
        "keywords": "创伤知情,PTSD,创伤,安全感,赋权,二次创伤",
        "source": "SAMHSA (2014). Trauma-Informed Care in Behavioral Health Services.",
        "reliability_score": 10
    },
    {
        "title": "创伤稳定化技术",
        "category": "intervention",
        "subcategory": "Trauma",
        "content": """在处理创伤前，必须先建立稳定和安全。稳定化技术包括：1) 安全感建立（内外部安全资源）；2) 情绪调节技能（呼吸、接地技术）；3) 资源建立（回忆积极体验、想象安全地点）；4) 心理教育（解释创伤反应的正常性）。遵循"稳定-处理-整合"三阶段模型，不在稳定前强行暴露创伤记忆。""",
        "keywords": "创伤稳定化,安全资源,情绪调节,接地技术,PTSD治疗",
        "source": "Herman, J. L. (1992). Trauma and Recovery.",
        "reliability_score": 10
    },
    {
        "title": "接地技术（Grounding）",
        "category": "technique",
        "subcategory": "Trauma",
        "content": """接地技术帮助创伤幸存者从闪回或解离状态回到当下。常用方法：1) 5-4-3-2-1 感官觉察（说出5样看到的、4样摸到的、3样听到的、2样闻到的、1样尝到的）；2) 脚踩地面，感受与大地的连接；3) 握冰块或摸粗糙物品；4) 命名周围物品。这些技术激活感官系统，将注意力从创伤记忆转移到当下现实。""",
        "keywords": "接地技术,闪回,解离,PTSD,当下觉察,感官练习",
        "source": "Najavits, L. M. (2002). Seeking Safety.",
        "reliability_score": 9
    },
    
    # ========== 人际关系 ==========
    {
        "title": "Gottman 四骑士理论",
        "category": "theory",
        "subcategory": "Relationships",
        "content": """心理学家 Gottman 研究发现，四种沟通模式（称为"四骑士"）预示关系破裂：1) 批评（Criticism）：攻击对方性格而非行为；2) 蔑视（Contempt）：讽刺、嘲笑、居高临下；3) 防御（Defensiveness）：推卸责任、反击；4) 冷战（Stonewalling）：退缩、沉默、拒绝交流。改善关系需用软化启动、建立情感联结、接受影响、修复尝试等技巧。""",
        "keywords": "Gottman,四骑士,亲密关系,沟通,婚姻,冲突",
        "source": "Gottman, J. M. (1994). Why Marriages Succeed or Fail.",
        "reliability_score": 10
    },
    {
        "title": "非暴力沟通（NVC）",
        "category": "technique",
        "subcategory": "Communication",
        "content": """非暴力沟通（NVC）由罗森伯格创立，包括四要素：1) 观察（Observation）：客观描述事实，不评判；2) 感受（Feeling）：表达自己的真实感受；3) 需要（Need）：说出感受背后的需要；4) 请求（Request）：提出具体、可行的请求。例如："当你昨晚没打电话（观察），我感到担心（感受），因为我需要知道你平安（需要），你能不能以后晚归时发个短信？（请求）"。""",
        "keywords": "非暴力沟通,NVC,沟通技巧,情感表达,人际关系,冲突解决",
        "source": "Rosenberg, M. B. (2003). Nonviolent Communication.",
        "reliability_score": 9
    },
    
    # ========== 焦虑与恐慌 ==========
    {
        "title": "焦虑的认知模型",
        "category": "theory",
        "subcategory": "Anxiety",
        "content": """焦虑的认知模型认为，焦虑源于对威胁的过度评估和对自身应对能力的低估。个体倾向于灾难化思维、过度关注身体感觉（健康焦虑）、或预期未来危险（广泛性焦虑）。治疗包括：识别和挑战灾难化思维、暴露疗法（逐步面对恐惧）、减少安全行为（如反复检查）。""",
        "keywords": "焦虑,认知模型,灾难化思维,暴露疗法,安全行为,GAD",
        "source": "Clark, D. A., & Beck, A. T. (2010). Cognitive Therapy of Anxiety Disorders.",
        "reliability_score": 10
    },
    {
        "title": "渐进式肌肉放松（PMR）",
        "category": "technique",
        "subcategory": "Anxiety",
        "content": """渐进式肌肉放松由雅各布森创立，通过系统地紧张和放松各肌肉群来减轻焦虑。步骤：1) 找舒适姿势；2) 紧张某一肌肉群（如握拳）5-7秒；3) 快速放松，感受紧张与放松的对比；4) 从手部逐步移动到全身。每天练习15-20分钟，可降低整体焦虑水平和肌肉紧张。""",
        "keywords": "肌肉放松,PMR,焦虑缓解,放松训练,压力管理",
        "source": "Jacobson, E. (1938). Progressive Relaxation.",
        "reliability_score": 9
    },
    {
        "title": "暴露疗法治疗恐惧症",
        "category": "intervention",
        "subcategory": "Anxiety",
        "content": """暴露疗法是治疗恐惧症和焦虑障碍的金标准。原理：通过逐步、重复接触恐惧对象（而不发生预期的灾难），打破回避循环，实现习惯化。类型：1) 想象暴露（在脑海中想象）；2) 现场暴露（真实接触）；3) 虚拟现实暴露。关键是构建恐惧阶梯（从最小恐惧到最大恐惧），逐级暴露，停留足够时间直到焦虑下降。""",
        "keywords": "暴露疗法,恐惧症,焦虑,系统脱敏,习惯化,PTSD",
        "source": "Foa, E. B., et al. (2007). Prolonged Exposure Therapy for PTSD.",
        "reliability_score": 10
    },
    
    # ========== 抑郁 ==========
    {
        "title": "抑郁的认知三角",
        "category": "theory",
        "subcategory": "Depression",
        "content": """贝克的认知理论认为，抑郁个体存在"认知三角"：1) 对自己的负面看法（"我没用"）；2) 对世界的负面看法（"世界很糟糕"）；3) 对未来的负面看法（"不会好转"）。这些负面图式导致选择性注意、记忆偏差，维持抑郁。治疗通过挑战这些消极信念、收集反证、进行行为实验来改变认知。""",
        "keywords": "抑郁,认知三角,负性认知,贝克,认知图式,CBT",
        "source": "Beck, A. T. (1967). Depression: Clinical, Experimental, and Theoretical Aspects.",
        "reliability_score": 10
    },
    {
        "title": "抑郁的行为理论与行为激活",
        "category": "intervention",
        "subcategory": "Depression",
        "content": """行为理论认为抑郁源于积极强化减少和消极强化增加。个体回避活动→失去愉悦和成就感→更抑郁→更回避，形成恶性循环。行为激活打破这一循环：1) 监测活动和心情；2) 识别回避模式；3) 安排愉快活动和掌握性活动；4) 即使不想做也要做（行动先于动机）。研究显示行为激活效果与认知治疗相当。""",
        "keywords": "抑郁,行为激活,回避,愉快活动,掌握性活动,动机",
        "source": "Martell, C. R., et al. (2001). Behavioral Activation for Depression.",
        "reliability_score": 9
    },
    
    # ========== 完美主义与拖延 ==========
    {
        "title": "完美主义的类型与影响",
        "category": "theory",
        "subcategory": "Perfectionism",
        "content": """完美主义分为适应性和不适应性。不适应性完美主义特征：1) 设定不切实际的高标准；2) 过度关注错误；3) 对批评高度敏感；4) 全或无思维；5) 自我价值依赖于成就。这导致焦虑、抑郁、拖延、倦怠。治疗包括：识别完美主义信念、设定现实目标、练习自我同情、允许犯错。""",
        "keywords": "完美主义,自我批评,焦虑,拖延,自我同情,高标准",
        "source": "Shafran, R., et al. (2002). Clinical perfectionism: A cognitive–behavioural analysis.",
        "reliability_score": 9
    },
    {
        "title": "拖延的心理机制",
        "category": "theory",
        "subcategory": "Procrastination",
        "content": """拖延不是时间管理问题，而是情绪调节问题。人们拖延是为了逃避与任务相关的负面情绪（焦虑、无聊、挫败感）。短期获得缓解，长期加剧焦虑和自责。治疗策略：1) 识别引发拖延的情绪；2) 将任务分解为小步骤；3) 使用"5分钟规则"（先做5分钟）；4) 练习自我同情而非自我批评；5) 挑战完美主义。""",
        "keywords": "拖延,情绪调节,回避,焦虑,完美主义,自我同情",
        "source": "Sirois, F., & Pychyl, T. (2013). Procrastination and the Priority of Short-Term Mood Regulation.",
        "reliability_score": 9
    },
    
    # ========== 自我同情 ==========
    {
        "title": "自我同情的三要素",
        "category": "theory",
        "subcategory": "Self-Compassion",
        "content": """克里斯汀·内夫提出自我同情包括三要素：1) 自我善待（Self-Kindness）：对自己温柔而非严厉批判；2) 共同人性（Common Humanity）：认识到痛苦和不完美是人类共同经历；3) 正念（Mindfulness）：以平衡方式觉察痛苦，不过度认同也不压抑。研究显示自我同情与更少的焦虑抑郁、更高的幸福感和心理韧性相关。""",
        "keywords": "自我同情,自我善待,共同人性,正念,心理韧性,自我批评",
        "source": "Neff, K. D. (2003). Self-Compassion: An Alternative Conceptualization.",
        "reliability_score": 10
    },
    {
        "title": "自我同情练习",
        "category": "technique",
        "subcategory": "Self-Compassion",
        "content": """自我同情短练习：当你痛苦时，试着：1) 觉察痛苦（"这很痛苦"）；2) 记住共同人性（"痛苦是生活的一部分，我不是唯一经历这个的人"）；3) 对自己说温暖的话（"愿我善待自己"、"愿我给自己需要的同情"）。也可以将手放在心口，感受温暖和安慰。每天练习可逐渐降低自我批评，提升情绪韧性。""",
        "keywords": "自我同情练习,自我关怀,情绪调节,自我批评,心理韧性",
        "source": "Neff, K. D., & Germer, C. K. (2013). Self-Compassion in Clinical Practice.",
        "reliability_score": 9
    },
]


def get_role_knowledge_mapping():
    """
    定义每个角色应该关联哪些知识（通过知识标题匹配）
    返回格式：{role_name: [(knowledge_title, priority), ...]}
    """
    return {
        "认知教练·理查德": [
            ("认知行为疗法（CBT）核心原理", 10),
            ("认知扭曲的常见类型", 10),
            ("行为激活治疗抑郁", 9),
            ("焦虑的认知模型", 9),
            ("抑郁的认知三角", 9),
            ("完美主义的类型与影响", 8),
            ("拖延的心理机制", 8),
        ],
        "正念导师·静心": [
            ("正念减压（MBSR）基本原理", 10),
            ("正念呼吸练习", 10),
            ("接纳承诺疗法（ACT）核心", 9),
            ("渐进式肌肉放松（PMR）", 8),
            ("自我同情的三要素", 9),
            ("自我同情练习", 8),
        ],
        "积极心理师·阳光": [
            ("PERMA 幸福模型", 10),
            ("性格优势识别", 10),
            ("感恩练习", 9),
            ("自我同情的三要素", 8),
        ],
        "情绪专家·心涟": [
            ("情绪聚焦疗法（EFT）核心理念", 10),
            ("空椅子技术", 9),
            ("非暴力沟通（NVC）", 9),
            ("自我同情的三要素", 8),
        ],
        "创伤疗愈师·守护": [
            ("创伤知情护理原则", 10),
            ("创伤稳定化技术", 10),
            ("接地技术（Grounding）", 10),
            ("暴露疗法治疗恐惧症", 8),
        ],
        "青少年导师·星辰": [
            ("认知扭曲的常见类型", 8),
            ("自我同情的三要素", 9),
            ("自我同情练习", 8),
            ("完美主义的类型与影响", 8),
            ("拖延的心理机制", 8),
        ],
        "职场心理顾问·行远": [
            ("完美主义的类型与影响", 9),
            ("拖延的心理机制", 9),
            ("渐进式肌肉放松（PMR）", 8),
            ("非暴力沟通（NVC）", 9),
            ("抑郁的行为理论与行为激活", 8),
        ],
        "关系咨询师·和鸣": [
            ("Gottman 四骑士理论", 10),
            ("非暴力沟通（NVC）", 10),
            ("情绪聚焦疗法（EFT）核心理念", 8),
            ("自我同情的三要素", 8),
        ],
        "生命意义探索者·启明": [
            ("PERMA 幸福模型", 8),
            ("接纳承诺疗法（ACT）核心", 10),
            ("抑郁的认知三角", 8),
            ("自我同情的三要素", 9),
        ],
        "温暖倾听者·艾米": [
            # 人本主义倾向，通用知识即可
            ("自我同情的三要素", 9),
            ("自我同情练习", 9),
            ("非暴力沟通（NVC）", 8),
            ("正念减压（MBSR）基本原理", 7),
        ]
    }

