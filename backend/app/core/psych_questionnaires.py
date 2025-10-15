"""
专业心理测评量表库
包含 10+ 种经过验证的心理学量表
"""

# ==================== 情绪与心境类 ====================

# PHQ-9: Patient Health Questionnaire-9 (抑郁自评量表)
PHQ9_QUESTIONS = [
    "在过去的两周里，您感到心情郁闷、沮丧或绝望吗？",
    "在过去的两周里，您对做事失去兴趣或乐趣了吗？",
    "在过去的两周里，您入睡困难、睡不安稳或睡得过多吗？",
    "在过去的两周里，您感到疲倦或没有活力吗？",
    "在过去的两周里，您食欲不振或吃得过多吗？",
    "在过去的两周里，您觉得自己很糟糕，觉得自己让家人失望，或觉得自己是个失败者吗？",
    "在过去的两周里，您对事物专注有困难吗（例如阅读报纸或看电视时）？",
    "在过去的两周里，您动作或说话变慢，或变得比平时更烦躁或坐立不安吗？",
    "在过去的两周里，您有想过死，或用某种方式伤害自己吗？"
]

# GAD-7: Generalized Anxiety Disorder-7 (广泛性焦虑量表)
GAD7_QUESTIONS = [
    "在过去的两周里，您感到紧张、焦虑或急躁吗？",
    "在过去的两周里，您无法停止或控制担忧吗？",
    "在过去的两周里，您对各种事情过度担忧吗？",
    "在过去的两周里，您很难放松下来吗？",
    "在过去的两周里，您感到坐立不安，难以静坐吗？",
    "在过去的两周里，您容易变得烦躁或容易生气吗？",
    "在过去的两周里，您感到害怕，好像有什么可怕的事情会发生吗？"
]

# PSS-10: Perceived Stress Scale-10 (压力知觉量表)
PSS10_QUESTIONS = [
    "在过去的一个月里，您有多频繁地感到意外发生的事情让您心烦？",
    "在过去的一个月里，您有多频繁地感到无法控制生活中重要的事情？",
    "在过去的一个月里，您有多频繁地感到紧张和压力？",
    "在过去的一个月里，您有多频繁地成功应对了生活中的烦恼？",  # 反向题
    "在过去的一个月里，您有多频繁地感到自己能有效地处理生活中发生的重要变化？",  # 反向题
    "在过去的一个月里，您有多频繁地对自己处理个人问题的能力感到有信心？",  # 反向题
    "在过去的一个月里，您有多频繁地感到事情正朝着您希望的方向发展？",  # 反向题
    "在过去的一个月里，您有多频繁地发现自己无法应付所有需要做的事情？",
    "在过去的一个月里，您有多频繁地能够控制生活中的烦恼？",  # 反向题
    "在过去的一个月里，您有多频繁地感到无法掌控一切？"
]

# PANAS: Positive and Negative Affect Schedule (积极消极情绪量表)
PANAS_QUESTIONS = [
    "在过去一周里，您感到有兴趣的程度如何？",  # P
    "在过去一周里，您感到痛苦的程度如何？",  # N
    "在过去一周里，您感到兴奋的程度如何？",  # P
    "在过去一周里，您感到心烦的程度如何？",  # N
    "在过去一周里，您感到坚强的程度如何？",  # P
    "在过去一周里，您感到内疚的程度如何？",  # N
    "在过去一周里，您感到害怕的程度如何？",  # N
    "在过去一周里，您感到热情的程度如何？",  # P
    "在过去一周里，您感到骄傲的程度如何？",  # P
    "在过去一周里，您感到易怒的程度如何？",  # N
    "在过去一周里，您感到警觉的程度如何？",  # P
    "在过去一周里，您感到羞愧的程度如何？",  # N
    "在过去一周里，您感到受鼓舞的程度如何？",  # P
    "在过去一周里，您感到紧张的程度如何？",  # N
    "在过去一周里，您感到果断的程度如何？",  # P
    "在过去一周里，您感到注意力不集中的程度如何？",  # N
    "在过去一周里，您感到活跃的程度如何？",  # P
    "在过去一周里，您感到害怕的程度如何？",  # N
    "在过去一周里，您感到专注的程度如何？",  # P
    "在过去一周里，您感到敌对的程度如何？"  # N
]

# ==================== 人际关系类 ====================

# ECR-12: Experiences in Close Relationships-12 (亲密关系体验量表简版)
ECR12_QUESTIONS = [
    "我担心我会失去伴侣的爱。",  # 焦虑
    "我担心伴侣不会像我在乎TA那样在乎我。",  # 焦虑
    "我经常担心伴侣并不是真的爱我。",  # 焦虑
    "我担心伴侣会离开我。",  # 焦虑
    "我经常希望伴侣的感情能和我的一样强烈。",  # 焦虑
    "我很少担心伴侣会离开我。",  # 焦虑-反向
    "我不太愿意与伴侣分享我的内心感受。",  # 回避
    "我觉得向伴侣倾诉是很容易的。",  # 回避-反向
    "当需要依靠伴侣时，我感到很自在。",  # 回避-反向
    "我发现很难完全信任我的伴侣。",  # 回避
    "我向伴侣倾诉几乎所有的事情。",  # 回避-反向
    "我更愿意不向伴侣展示我内心深处的感受。"  # 回避
]

# IRI: Interpersonal Reactivity Index (人际反应指数 - 共情能力)
IRI_QUESTIONS = [
    "当朋友遇到问题时，我会尝试从TA的角度去看待问题。",  # 观点采择
    "我经常关心那些不如我幸运的人。",  # 共情关注
    "当看到有人被利用时，我会感到需要保护TA。",  # 共情关注
    "我能很容易地看到别人的立场，即使我不同意。",  # 观点采择
    "当我看到有人需要帮助时，我会立即提供帮助。",  # 共情关注
    "在做决定之前，我会尝试考虑每个人的观点。",  # 观点采择
    "看到别人受到不公平对待会让我难过。",  # 共情关注
    "我发现自己很难理解别人的观点。",  # 观点采择-反向
    "其他人的不幸并不会让我太困扰。",  # 共情关注-反向
    "我认为每个问题都有两面性，我会尝试看到两面。"  # 观点采择
]

# ==================== 自我认知类 ====================

# RSES: Rosenberg Self-Esteem Scale (罗森伯格自尊量表)
RSES_QUESTIONS = [
    "总的来说，我对自己感到满意。",
    "有时候，我觉得自己一无是处。",  # 反向
    "我觉得自己有许多优点。",
    "我能做事和大多数人一样好。",
    "我觉得自己没有太多值得骄傲的地方。",  # 反向
    "有时候我确实觉得自己很没用。",  # 反向
    "我觉得自己是一个有价值的人，至少和其他人一样有价值。",
    "我希望我能更加尊重自己。",  # 反向
    "总的来说，我倾向于认为自己是个失败者。",  # 反向
    "我对自己持积极态度。"
]

# SCS: Self-Compassion Scale (自我同情量表简版)
SCS_QUESTIONS = [
    "当我失败时，我会尽量以善意和理解的态度看待事情。",  # 自我友善
    "当我感到痛苦时，我会对自己过分苛刻和批判。",  # 自我批判-反向
    "当某些事情让我感到痛苦时，我试图以平衡的视角看待情况。",  # 正念
    "当我感到沮丧时，我倾向于觉得大多数人可能比我快乐。",  # 孤立-反向
    "当我失败时，我试图提醒自己失败是人类共同经验的一部分。",  # 普遍人性
    "当我经历痛苦时，我对自己非常不耐烦和不满。",  # 自我批判-反向
    "当我情绪低落时，我会提醒自己世界上很多人也有类似的感受。",  # 普遍人性
    "在艰难时期，我倾向于对自己温柔一些。",  # 自我友善
    "当发生不好的事情时，我倾向于专注于错误而不是整体情况。",  # 过度认同-反向
    "当我失败或感觉不足时，我试图保持情绪的平衡。",  # 正念
    "当我感到不足时，我会试图以关心和温柔的态度对待自己。",  # 自我友善
    "当我感到沮丧时，我倾向于沉迷于一切错误。"  # 过度认同-反向
]

# ==================== 职场与学业类 ====================

# MBI-GS: Maslach Burnout Inventory - General Survey (职业倦怠量表简版)
MBI_GS_QUESTIONS = [
    "我在工作/学习后感到精疲力竭。",  # 情绪耗竭
    "我在早晨醒来面对新的一天工作/学习时感到疲倦。",  # 情绪耗竭
    "我在工作/学习一整天后感到筋疲力尽。",  # 情绪耗竭
    "我对工作/学习失去了热情。",  # 去人格化
    "我对我的工作/学习不再像以前那样投入。",  # 去人格化
    "我怀疑我的工作/学习的意义。",  # 去人格化
    "我能有效地解决工作/学习中出现的问题。",  # 个人成就感-反向
    "我觉得我在为组织/学校做出有效的贡献。",  # 个人成就感-反向
    "我对我所做的工作/学习感到自豪。"  # 个人成就感-反向
]

# ==================== 创伤与应激类 ====================

# PCL-5: PTSD Checklist for DSM-5 (创伤后应激障碍检查表简版)
PCL5_QUESTIONS = [
    "在过去一个月里，您有多频繁地被不想要的痛苦记忆所困扰？",
    "在过去一个月里，您有多频繁地做关于创伤性事件的噩梦？",
    "在过去一个月里，您有多频繁地突然感觉或表现得好像创伤性事件又发生了一样？",
    "在过去一个月里，当您想起创伤性事件时，您感到多频繁的心烦意乱？",
    "在过去一个月里，您有多频繁地避免与创伤性事件有关的记忆、想法或感受？",
    "在过去一个月里，您有多频繁地避免与创伤性事件相关的外部提醒（人、地方、对话、活动、物品或情境）？",
    "在过去一个月里，您有多频繁地无法记住创伤性事件的重要部分？",
    "在过去一个月里，您有多频繁地对自己、他人或世界持有强烈的负面信念（例如：我很糟糕、没有人可以信任、世界是完全危险的）？",
    "在过去一个月里，您有多频繁地难以感受到积极情绪（例如快乐、满足或爱的感觉）？",
    "在过去一个月里，您有多频繁地感到过度警觉或易受惊吓？"
]

# ==================== 选项定义 ====================

# 4点量表 (PHQ-9, GAD-7 使用)
OPTIONS_4POINT_FREQUENCY = [
    {"text": "完全没有", "score": 0},
    {"text": "有几天", "score": 1},
    {"text": "一半以上天数", "score": 2},
    {"text": "几乎每天", "score": 3}
]

# 5点量表 (PSS-10, PANAS, PCL-5 使用)
OPTIONS_5POINT_FREQUENCY = [
    {"text": "从不", "score": 0},
    {"text": "几乎从不", "score": 1},
    {"text": "有时", "score": 2},
    {"text": "经常", "score": 3},
    {"text": "总是", "score": 4}
]

# 5点量表 - 程度 (PANAS 使用)
OPTIONS_5POINT_DEGREE = [
    {"text": "完全不", "score": 1},
    {"text": "有一点", "score": 2},
    {"text": "中等程度", "score": 3},
    {"text": "相当多", "score": 4},
    {"text": "非常", "score": 5}
]

# 7点量表 (ECR-12, IRI, RSES, SCS, MBI-GS 使用)
OPTIONS_7POINT_AGREEMENT = [
    {"text": "完全不同意", "score": 1},
    {"text": "不同意", "score": 2},
    {"text": "有点不同意", "score": 3},
    {"text": "中立", "score": 4},
    {"text": "有点同意", "score": 5},
    {"text": "同意", "score": 6},
    {"text": "完全同意", "score": 7}
]

# ==================== 量表配置 ====================

QUESTIONNAIRES = {
    "PHQ9": {
        "title": "PHQ-9 抑郁自评量表",
        "abbr": "PHQ-9",
        "category": "情绪与心境",
        "description": "评估过去两周的抑郁症状严重程度",
        "time": "3-5分钟",
        "questions": PHQ9_QUESTIONS,
        "options": OPTIONS_4POINT_FREQUENCY,
        "reverse_items": [],
        "scoring_type": "sum",
        "interpretation": {
            "ranges": [
                {"min": 0, "max": 4, "level": "无/极轻微", "color": "green", "advice": "无抑郁症状或极轻微。建议保持良好心态，继续维护心理健康。"},
                {"min": 5, "max": 9, "level": "轻度", "color": "yellow", "advice": "轻度抑郁。建议适当放松，关注自我情绪，考虑通过运动、冥想等方式调节。"},
                {"min": 10, "max": 14, "level": "中度", "color": "orange", "advice": "中度抑郁。建议寻求心理支持，可考虑与平台的专业 AI 心理咨询师深度对话，必要时咨询线下专业人士。"},
                {"min": 15, "max": 19, "level": "中重度", "color": "red", "advice": "中重度抑郁。强烈建议尽快寻求专业心理帮助或精神科医生的评估和治疗。"},
                {"min": 20, "max": 27, "level": "重度", "color": "red", "advice": "重度抑郁。请立即联系专业心理医生或精神科医生，必要时拨打心理危机热线（如 12320）。"}
            ]
        }
    },
    "GAD7": {
        "title": "GAD-7 焦虑自评量表",
        "abbr": "GAD-7",
        "category": "情绪与心境",
        "description": "评估过去两周的焦虑症状严重程度",
        "time": "2-4分钟",
        "questions": GAD7_QUESTIONS,
        "options": OPTIONS_4POINT_FREQUENCY,
        "reverse_items": [],
        "scoring_type": "sum",
        "interpretation": {
            "ranges": [
                {"min": 0, "max": 4, "level": "无/极轻微", "color": "green", "advice": "无焦虑症状或极轻微。建议保持良好心态。"},
                {"min": 5, "max": 9, "level": "轻度", "color": "yellow", "advice": "轻度焦虑。建议适当放松，关注自我情绪，尝试深呼吸、正念等放松技巧。"},
                {"min": 10, "max": 14, "level": "中度", "color": "orange", "advice": "中度焦虑。建议寻求心理支持，学习焦虑管理技巧，必要时咨询专业人士。"},
                {"min": 15, "max": 21, "level": "重度", "color": "red", "advice": "重度焦虑。建议尽快寻求专业心理帮助或精神科医生的评估。"}
            ]
        }
    },
    "PSS10": {
        "title": "PSS-10 压力知觉量表",
        "abbr": "PSS-10",
        "category": "情绪与心境",
        "description": "评估过去一个月的主观压力水平",
        "time": "3-5分钟",
        "questions": PSS10_QUESTIONS,
        "options": OPTIONS_5POINT_FREQUENCY,
        "reverse_items": [3, 4, 5, 6, 8],  # 反向计分题目（索引从0开始，所以是第4,5,6,7,9题）
        "scoring_type": "sum",
        "interpretation": {
            "ranges": [
                {"min": 0, "max": 13, "level": "低压力", "color": "green", "advice": "压力水平较低，您的应对能力良好。建议继续保持健康的生活方式和积极的应对策略。"},
                {"min": 14, "max": 26, "level": "中等压力", "color": "yellow", "advice": "中等压力水平。建议学习压力管理技巧，如时间管理、放松训练、适度运动等。"},
                {"min": 27, "max": 40, "level": "高压力", "color": "red", "advice": "高压力水平。强烈建议寻求专业心理支持，学习有效的压力应对策略，必要时考虑心理咨询。"}
            ]
        }
    },
    "PANAS": {
        "title": "PANAS 积极消极情绪量表",
        "abbr": "PANAS",
        "category": "情绪与心境",
        "description": "评估过去一周的积极和消极情绪状态",
        "time": "5-7分钟",
        "questions": PANAS_QUESTIONS,
        "options": OPTIONS_5POINT_DEGREE,
        "reverse_items": [],
        "scoring_type": "subscale",  # 分量表计分
        "subscales": {
            "positive": {"name": "积极情绪", "items": [0, 2, 4, 7, 8, 10, 12, 14, 16, 18]},  # 奇数项
            "negative": {"name": "消极情绪", "items": [1, 3, 5, 6, 9, 11, 13, 15, 17, 19]}  # 偶数项
        },
        "interpretation": {
            "positive": [
                {"min": 10, "max": 25, "level": "低积极情绪", "color": "yellow", "advice": "积极情绪较低。建议增加愉快活动，培养感恩习惯，与朋友多交流。"},
                {"min": 26, "max": 35, "level": "中等积极情绪", "color": "green", "advice": "积极情绪处于正常范围。继续保持，可以尝试更多带来快乐的活动。"},
                {"min": 36, "max": 50, "level": "高积极情绪", "color": "green", "advice": "积极情绪丰富，这对心理健康非常有益！"}
            ],
            "negative": [
                {"min": 10, "max": 18, "level": "低消极情绪", "color": "green", "advice": "消极情绪较少，心理状态良好。"},
                {"min": 19, "max": 28, "level": "中等消极情绪", "color": "yellow", "advice": "存在一定程度的消极情绪。建议学习情绪调节技巧，如正念、认知重构等。"},
                {"min": 29, "max": 50, "level": "高消极情绪", "color": "red", "advice": "消极情绪较高。建议寻求心理支持，学习有效的情绪管理策略。"}
            ]
        }
    },
    "ECR12": {
        "title": "ECR-12 亲密关系体验量表",
        "abbr": "ECR-12",
        "category": "人际关系",
        "description": "评估亲密关系中的依恋风格（焦虑与回避）",
        "time": "4-6分钟",
        "questions": ECR12_QUESTIONS,
        "options": OPTIONS_7POINT_AGREEMENT,
        "reverse_items": [5, 7, 8, 10],  # 第6, 8, 9, 11题反向
        "scoring_type": "subscale",
        "subscales": {
            "anxiety": {"name": "关系焦虑", "items": [0, 1, 2, 3, 4, 5]},
            "avoidance": {"name": "关系回避", "items": [6, 7, 8, 9, 10, 11]}
        },
        "interpretation": {
            "anxiety": [
                {"min": 6, "max": 20, "level": "低焦虑", "color": "green", "advice": "在亲密关系中焦虑水平较低，能够安心信任伴侣。"},
                {"min": 21, "max": 35, "level": "中等焦虑", "color": "yellow", "advice": "存在一定的关系焦虑。建议与伴侣坦诚沟通，建立安全感。"},
                {"min": 36, "max": 42, "level": "高焦虑", "color": "red", "advice": "关系焦虑较高，可能过度担心被抛弃。建议寻求关系咨询或个人咨询。"}
            ],
            "avoidance": [
                {"min": 6, "max": 15, "level": "低回避", "color": "green", "advice": "在亲密关系中回避程度低，愿意亲密和依赖。"},
                {"min": 16, "max": 30, "level": "中等回避", "color": "yellow", "advice": "存在一定的关系回避倾向。建议尝试逐步增加亲密度和信任。"},
                {"min": 31, "max": 42, "level": "高回避", "color": "red", "advice": "关系回避程度较高，可能难以建立深度亲密。建议探索亲密恐惧的根源。"}
            ]
        }
    },
    "IRI": {
        "title": "IRI 人际反应指数（共情能力）",
        "abbr": "IRI",
        "category": "人际关系",
        "description": "评估共情能力（观点采择与共情关注）",
        "time": "3-5分钟",
        "questions": IRI_QUESTIONS,
        "options": OPTIONS_7POINT_AGREEMENT,
        "reverse_items": [7, 8],  # 第8, 9题反向
        "scoring_type": "subscale",
        "subscales": {
            "perspective": {"name": "观点采择", "items": [0, 3, 5, 7, 9]},
            "empathic": {"name": "共情关注", "items": [1, 2, 4, 6, 8]}
        },
        "interpretation": {
            "perspective": [
                {"min": 5, "max": 20, "level": "低观点采择", "color": "yellow", "advice": "观点采择能力较低。建议练习从他人角度思考问题。"},
                {"min": 21, "max": 28, "level": "中等观点采择", "color": "green", "advice": "观点采择能力正常。"},
                {"min": 29, "max": 35, "level": "高观点采择", "color": "green", "advice": "观点采择能力强，善于理解他人立场。"}
            ],
            "empathic": [
                {"min": 5, "max": 18, "level": "低共情关注", "color": "yellow", "advice": "共情关注较低。建议增加对他人感受的关注。"},
                {"min": 19, "max": 27, "level": "中等共情关注", "color": "green", "advice": "共情关注正常，能够关心他人。"},
                {"min": 28, "max": 35, "level": "高共情关注", "color": "green", "advice": "共情关注能力强，富有同情心和关怀。"}
            ]
        }
    },
    "RSES": {
        "title": "RSES 罗森伯格自尊量表",
        "abbr": "RSES",
        "category": "自我认知",
        "description": "评估整体自尊水平",
        "time": "2-4分钟",
        "questions": RSES_QUESTIONS,
        "options": OPTIONS_7POINT_AGREEMENT,
        "reverse_items": [1, 4, 5, 7, 8],  # 第2, 5, 6, 8, 9题反向
        "scoring_type": "sum",
        "interpretation": {
            "ranges": [
                {"min": 10, "max": 30, "level": "低自尊", "color": "red", "advice": "自尊水平较低。建议探索自我价值感的来源，寻求心理咨询以提升自尊。"},
                {"min": 31, "max": 50, "level": "中等自尊", "color": "yellow", "advice": "自尊水平处于中等范围。可以通过肯定自己的成就和优点来进一步提升。"},
                {"min": 51, "max": 70, "level": "高自尊", "color": "green", "advice": "自尊水平良好，对自己有积极的评价。"}
            ]
        }
    },
    "SCS": {
        "title": "SCS 自我同情量表",
        "abbr": "SCS",
        "category": "自我认知",
        "description": "评估对自己的友善、正念和普遍人性的理解",
        "time": "4-6分钟",
        "questions": SCS_QUESTIONS,
        "options": OPTIONS_7POINT_AGREEMENT,
        "reverse_items": [1, 3, 5, 8],  # 反向题
        "scoring_type": "average",  # 平均分
        "interpretation": {
            "ranges": [
                {"min": 1.0, "max": 2.5, "level": "低自我同情", "color": "red", "advice": "自我同情水平较低，对自己可能过于苛刻。建议学习自我关怀技巧，用对待朋友的方式对待自己。"},
                {"min": 2.6, "max": 3.5, "level": "中等自我同情", "color": "yellow", "advice": "自我同情处于中等水平。可以继续练习在困难时对自己更友善。"},
                {"min": 3.6, "max": 5.0, "level": "高自我同情", "color": "green", "advice": "自我同情水平良好，能够在困难时善待自己。"},
                {"min": 5.1, "max": 7.0, "level": "非常高自我同情", "color": "green", "advice": "自我同情能力很强，这对心理健康非常有益。"}
            ]
        }
    },
    "MBI_GS": {
        "title": "MBI-GS 职业倦怠量表",
        "abbr": "MBI-GS",
        "category": "职场与学业",
        "description": "评估工作/学习倦怠程度（情绪耗竭、去人格化、个人成就感）",
        "time": "3-5分钟",
        "questions": MBI_GS_QUESTIONS,
        "options": OPTIONS_7POINT_AGREEMENT,
        "reverse_items": [6, 7, 8],  # 个人成就感题目反向计分
        "scoring_type": "subscale",
        "subscales": {
            "exhaustion": {"name": "情绪耗竭", "items": [0, 1, 2]},
            "cynicism": {"name": "去人格化", "items": [3, 4, 5]},
            "efficacy": {"name": "个人成就感", "items": [6, 7, 8]}
        },
        "interpretation": {
            "exhaustion": [
                {"min": 3, "max": 10, "level": "低耗竭", "color": "green", "advice": "情绪耗竭程度低，精力充沛。"},
                {"min": 11, "max": 15, "level": "中等耗竭", "color": "yellow", "advice": "存在一定程度的情绪耗竭。建议注意工作-生活平衡，增加休息和放松时间。"},
                {"min": 16, "max": 21, "level": "高耗竭", "color": "red", "advice": "情绪耗竭严重。强烈建议寻求支持，调整工作节奏，必要时考虑职业咨询。"}
            ],
            "cynicism": [
                {"min": 3, "max": 9, "level": "低去人格化", "color": "green", "advice": "对工作保持热情和投入。"},
                {"min": 10, "max": 14, "level": "中等去人格化", "color": "yellow", "advice": "开始对工作感到疏离。建议重新连接工作的意义和价值。"},
                {"min": 15, "max": 21, "level": "高去人格化", "color": "red", "advice": "对工作严重疏离和怀疑。建议寻求职业咨询，探索职业意义。"}
            ],
            "efficacy": [
                {"min": 3, "max": 10, "level": "低成就感", "color": "red", "advice": "个人成就感低。建议关注自己的成就，寻求反馈和认可。"},
                {"min": 11, "max": 15, "level": "中等成就感", "color": "yellow", "advice": "成就感中等。可以设定清晰的目标并庆祝小成就。"},
                {"min": 16, "max": 21, "level": "高成就感", "color": "green", "advice": "成就感良好，对工作有效能感。"}
            ]
        }
    },
    "PCL5": {
        "title": "PCL-5 PTSD检查表",
        "abbr": "PCL-5",
        "category": "创伤与应激",
        "description": "评估创伤后应激障碍（PTSD）症状（简版）",
        "time": "3-5分钟",
        "questions": PCL5_QUESTIONS,
        "options": OPTIONS_5POINT_FREQUENCY,
        "reverse_items": [],
        "scoring_type": "sum",
        "interpretation": {
            "ranges": [
                {"min": 0, "max": 10, "level": "无/极轻微PTSD症状", "color": "green", "advice": "创伤后应激症状极轻微或没有。如果曾经历创伤，说明恢复良好。"},
                {"min": 11, "max": 20, "level": "轻度PTSD症状", "color": "yellow", "advice": "存在轻度创伤后应激症状。建议关注自我照顾，必要时寻求心理支持。"},
                {"min": 21, "max": 30, "level": "中度PTSD症状", "color": "orange", "advice": "中度创伤后应激症状。建议寻求专业创伤治疗（如 EMDR、TF-CBT）。"},
                {"min": 31, "max": 40, "level": "重度PTSD症状", "color": "red", "advice": "重度创伤后应激症状。强烈建议立即寻求专业创伤治疗和精神科评估。"}
            ]
        }
    }
}


def get_test_categories():
    """获取所有测评分类"""
    categories = {}
    for key, config in QUESTIONNAIRES.items():
        cat = config["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "key": key,
            "title": config["title"],
            "abbr": config["abbr"],
            "description": config["description"],
            "time": config["time"]
        })
    return categories

