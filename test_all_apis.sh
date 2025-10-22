#!/bin/bash

echo "======================================"
echo "  Hai 后端 API 全面测试"
echo "======================================"
echo ""

BASE_URL="http://localhost:8000/api"
USER_ID=6

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_api() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=$4
    
    echo -n "测试 $name ... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s "$url")
    else
        response=$(curl -s -X "$method" "$url" -H "Content-Type: application/json" -d "$data")
    fi
    
    if echo "$response" | grep -q "detail.*Not Found"; then
        echo -e "${RED}❌ 404 Not Found${NC}"
        echo "   URL: $url"
        return 1
    elif echo "$response" | grep -q "Internal Server Error"; then
        echo -e "${RED}❌ 500 Internal Server Error${NC}"
        echo "   URL: $url"
        return 1
    elif [ -z "$response" ]; then
        echo -e "${RED}❌ 无响应${NC}"
        echo "   URL: $url"
        return 1
    else
        echo -e "${GREEN}✅ 成功${NC}"
        return 0
    fi
}

echo "【1. 用户相关 API】"
test_api "用户登录" "$BASE_URL/user/login" "POST" '{"username":"Hughhugh","password":"Zdybeyourself"}'
test_api "用户注册（已存在）" "$BASE_URL/user/register" "POST" '{"username":"Hughhugh","email":"test@example.com","password":"test123"}'
echo ""

echo "【2. AI 对话相关 API】"
test_api "获取AI角色列表" "$BASE_URL/ai/roles"
test_api "获取聊天历史" "$BASE_URL/ai/history?user_id=$USER_ID&role_id=1&limit=10"
echo ""

echo "【3. 心理测评相关 API】"
test_api "获取测评分类" "$BASE_URL/psych/categories"
test_api "获取测评问卷" "$BASE_URL/psych/questionnaire?test_type=phq9"
test_api "获取测评历史" "$BASE_URL/psych/history?user_id=$USER_ID"
echo ""

echo "【4. 打卡相关 API】"
test_api "获取打卡历史" "$BASE_URL/checkin/history?user_id=$USER_ID"
echo ""

echo "【5. 积分奖励相关 API】"
test_api "获取用户积分" "$BASE_URL/rewards/points?user_id=$USER_ID"
test_api "获取积分历史" "$BASE_URL/rewards/history?user_id=$USER_ID"
echo ""

echo "【6. 康复计划相关 API】"
test_api "获取作息配置" "$BASE_URL/plan/profile?user_id=$USER_ID"
test_api "获取计划历史" "$BASE_URL/plan/history?user_id=$USER_ID"
echo ""

echo "======================================"
echo "  测试完成"
echo "======================================"

