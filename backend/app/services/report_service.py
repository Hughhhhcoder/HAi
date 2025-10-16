"""
AI 测评报告生成服务
基于测评结果调用 AI 生成专业的心理评估报告
"""
import httpx
import os
from typing import Dict, Any
import json


def generate_assessment_report(test_type: str, score: int, result: Dict[str, Any], user_id: int) -> str:
    """
    调用 AI 生成专业测评报告
    
    Args:
        test_type: 测评类型（如 PHQ9, GAD7, ECR36 等）
        score: 主要得分
        result: 完整测评结果（包含分量表等）
        user_id: 用户ID
        
    Returns:
        str: AI 生成的专业报告
    """
    # 构建专业的提示词
    prompt = _build_report_prompt(test_type, score, result)
    
    # 调用外部 AI API
    try:
        ai_report = _call_ai_for_report(prompt)
        return ai_report
    except Exception as e:
        print(f"[ERROR] AI 报告生成失败: {e}")
        # 降级：返回基础建议
        return result.get("advice", "测评完成，建议关注心理健康。")


def _build_report_prompt(test_type: str, score: int, result: Dict[str, Any]) -> str:
    """构建 AI 报告生成的提示词"""
    
    # 获取测评的详细信息
    from app.core.psych_questionnaires import QUESTIONNAIRES
    config = QUESTIONNAIRES.get(test_type, {})
    
    test_title = config.get("title", test_type)
    test_abbr = config.get("abbr", test_type)
    category = config.get("category", "心理评估")
    
    # 基础信息
    prompt = f"""你是一位资深的临床心理学家和心理测评专家，拥有心理学博士学位和多年临床经验。请根据以下测评结果，生成一份专业、详细的心理评估报告。

## 测评信息
- **量表名称**: {test_title} ({test_abbr})
- **测评类别**: {category}
- **总分**: {score}分
- **评估等级**: {result.get('level', '未知')}

"""
    
    # 如果有分量表，添加详细信息
    if "subscores" in result:
        prompt += "## 分量表得分\n"
        for key, subscore in result.get("subscores", {}).items():
            prompt += f"- **{subscore.get('name', key)}**: {subscore.get('score')}分 - {subscore.get('level', '')}\n"
        prompt += "\n"
    
    # 报告要求
    prompt += """## 请生成包含以下内容的专业报告

### 1. 测评结果总结（50-80字）
用专业但易懂的语言概述测评结果的整体情况。

### 2. 详细解读（200-300字）
- 分析得分的心理学意义
- 解释可能的心理状态或特征
- 如有分量表，分析各维度的相互关系
- 基于国际诊断标准（如 DSM-5）或心理学理论进行解读

### 3. 心理健康建议（150-200字）
- 针对性的自我照顾建议
- 具体可操作的改善方法
- 推荐的心理技巧或练习
- 必要时建议寻求专业帮助的时机

### 4. 积极资源与优势（80-120字）
- 识别来访者的心理资源和优势
- 鼓励性的反馈
- 强化积极的应对方式

## 报告要求
1. **专业性**: 使用心理学专业术语，但确保普通人能理解
2. **客观性**: 基于测评结果，避免过度推断
3. **温暖性**: 语气专业但温暖，避免标签化或病理化
4. **实用性**: 提供具体可行的建议
5. **结构化**: 使用 Markdown 格式，清晰分段
6. **国际标准**: 参考 DSM-5、ICD-11 等国际诊断标准
7. **伦理性**: 强调测评是筛查工具，非临床诊断，必要时建议专业帮助

请直接输出专业报告内容，使用 Markdown 格式。"""
    
    return prompt


def _call_ai_for_report(prompt: str) -> str:
    """调用外部 AI API 生成报告"""
    
    # 从环境变量读取配置
    use_external = os.getenv("AI_USE_EXTERNAL", "false").lower() == "true"
    
    if not use_external:
        # 如果未启用外部 AI，返回简化报告
        return "## 测评完成\n\n您的测评已完成，建议关注心理健康状态。如需详细解读，请启用 AI 报告生成功能。"
    
    api_url = os.getenv("AI_API_URL", "https://api.openai.com/v1/chat/completions")
    api_key = os.getenv("AI_API_KEY", "")
    model = os.getenv("AI_MODEL", "gpt-4o-mini")
    
    if not api_key:
        print("[WARN] AI_API_KEY 未配置，无法生成 AI 报告")
        return "## 测评完成\n\n请配置 AI API 以启用专业报告生成。"
    
    # 构建请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "你是一位资深的临床心理学家和心理测评专家，擅长撰写专业的心理评估报告。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            report = data["choices"][0]["message"]["content"]
            
            print(f"[INFO] AI 报告生成成功，长度: {len(report)} 字符")
            return report
            
    except httpx.TimeoutException:
        print("[ERROR] AI 报告生成超时")
        return "## 报告生成超时\n\n由于网络原因，专业报告生成超时。您可以稍后重新测评或查看基础建议。"
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] AI API 返回错误: {e.response.status_code} - {e.response.text}")
        return "## 报告生成失败\n\n暂时无法生成专业报告，请稍后再试。"
    except Exception as e:
        print(f"[ERROR] AI 报告生成异常: {e}")
        return "## 报告生成失败\n\n发生未知错误，请联系管理员。"


def extract_key_findings_for_profile(test_type: str, score: int, result: Dict[str, Any]) -> str:
    """
    从测评结果中提取关键信息，用于更新用户画像
    
    Returns:
        str: 简洁的测评摘要，适合注入到用户画像中
    """
    from app.core.psych_questionnaires import QUESTIONNAIRES
    config = QUESTIONNAIRES.get(test_type, {})
    
    test_name = config.get("abbr", test_type)
    level = result.get("level", "未知")
    
    # 基础摘要
    summary = f"{test_name}测评: {level}({score}分)"
    
    # 如果有分量表，添加关键维度
    if "subscores" in result:
        subscores = result.get("subscores", {})
        key_dimensions = []
        
        for key, subscore in subscores.items():
            dim_name = subscore.get("name", key)
            dim_level = subscore.get("level", "")
            dim_score = subscore.get("score", 0)
            key_dimensions.append(f"{dim_name}={dim_level}({dim_score})")
        
        if key_dimensions:
            summary += " | " + ", ".join(key_dimensions[:3])  # 最多展示3个维度
    
    return summary

