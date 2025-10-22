#!/usr/bin/env python3
"""
测试心理测评结果是否真的能自动更新到用户画像
"""
import requests
import json

# 测试配置
BASE_URL = "http://localhost:8000"
USER_ID = 1

def test_psych_profile_update():
    print("🧪 测试心理测评结果自动更新到用户画像")
    print("=" * 50)
    
    # 1. 先查看用户当前画像
    print("\n1️⃣ 查看用户当前画像...")
    try:
        response = requests.get(f"{BASE_URL}/api/psych/profile/{USER_ID}")
        if response.status_code == 200:
            profile = response.json()
            print("✅ 当前用户画像:")
            print(f"   - 主要关注: {profile.get('main_concerns', '无')[:100]}...")
            print(f"   - 优势: {profile.get('strengths', '无')[:100]}...")
            print(f"   - 应对模式: {profile.get('coping_patterns', '无')[:100]}...")
        else:
            print(f"❌ 获取用户画像失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return
    
    # 2. 提交一个简单的心理测评
    print("\n2️⃣ 提交PHQ-9抑郁测评...")
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
        else:
            print(f"❌ 测评提交失败: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return
    
    # 3. 再次查看用户画像，看是否更新
    print("\n3️⃣ 查看更新后的用户画像...")
    try:
        response = requests.get(f"{BASE_URL}/api/psych/profile/{USER_ID}")
        if response.status_code == 200:
            profile = response.json()
            print("✅ 更新后的用户画像:")
            print(f"   - 主要关注: {profile.get('main_concerns', '无')[:200]}...")
            print(f"   - 优势: {profile.get('strengths', '无')[:200]}...")
            print(f"   - 应对模式: {profile.get('coping_patterns', '无')[:200]}...")
            print(f"   - 核心特质: {profile.get('core_traits', '无')[:200]}...")
            
            # 检查是否有新的测评信息
            main_concerns = profile.get('main_concerns', '')
            if 'PHQ-9' in main_concerns or '抑郁' in main_concerns:
                print("\n🎉 成功！测评结果已自动更新到用户画像")
            else:
                print("\n⚠️  警告：测评结果可能没有正确更新到用户画像")
        else:
            print(f"❌ 获取用户画像失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    test_psych_profile_update()
