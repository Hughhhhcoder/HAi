#!/usr/bin/env python3
"""
直接测试数据库中的用户画像更新
"""
import requests
import json

# 测试配置
BASE_URL = "http://localhost:8000"
USER_ID = 1

def test_direct_psych_submit():
    print("🧪 直接测试心理测评提交和画像更新")
    print("=" * 50)
    
    # 提交一个PHQ-9测评
    print("\n1️⃣ 提交PHQ-9抑郁测评...")
    test_data = {
        "user_id": USER_ID,
        "test_type": "PHQ9",
        "answers": [2, 2, 1, 2, 1, 2, 1, 1, 0]  # 模拟中度抑郁的答案
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/psych/submit", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 测评提交成功:")
            print(f"   - 总分: {result.get('total_score', 'N/A')}")
            print(f"   - 等级: {result.get('level', 'N/A')}")
            print(f"   - 建议: {result.get('suggestion', 'N/A')[:100]}...")
            print(f"   - AI报告: {'有' if result.get('ai_report') else '无'}")
            
            # 检查后端日志中是否有画像更新信息
            print("\n2️⃣ 检查后端日志...")
            print("请查看后端容器日志，应该看到类似以下信息：")
            print("   [INFO] 已将 PHQ9 测评结果同步到用户 1 的画像")
            print("   [INFO] 已更新用户 1 的专业测评画像，更新字段: ['main_concerns']")
            
        else:
            print(f"❌ 测评提交失败: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_direct_psych_submit()
