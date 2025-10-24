#!/bin/bash

# 测试本地多轮对话
# 使用方法: 
#   1. 先启动 app.py: python app.py
#   2. 然后运行此脚本: bash test_multi_turn_local.sh

set -e  # 遇到错误立即退出

# 服务地址
BASE_URL="http://localhost:8080"
ENDPOINT="${BASE_URL}/invocations"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "========================================================================"
echo -e "${GREEN}🚀 开始测试多轮对话${NC}"
echo "========================================================================"
echo ""

# 检查服务是否可用
echo -e "${CYAN}📡 检查服务状态...${NC}"
if curl -s -f "${BASE_URL}/ping" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 服务正常运行${NC}"
    echo ""
else
    echo -e "${RED}❌ 服务未启动！请先运行: python app.py${NC}"
    exit 1
fi

# 第1轮对话
echo "========================================================================"
echo -e "${BLUE}🗣️  第 1 轮对话${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 发送: Hello, agent! My name is Jason.${NC}"
echo ""

RESPONSE1=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{
        "prompt": "Hello, agent! My name is Jason.",
        "streaming": false
    }')

echo -e "${GREEN}📥 响应:${NC}"
echo "${RESPONSE1}" | jq -r '.result // .error // .'
echo ""
echo -e "${CYAN}⏳ 等待 2 秒后进入下一轮...${NC}"
sleep 2
echo ""

# 第2轮对话
echo "========================================================================"
echo -e "${BLUE}🗣️  第 2 轮对话${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 发送: Tell me something interesting about Elon Musk.${NC}"
echo ""

RESPONSE2=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{
        "prompt": "Tell me something interesting about Elon Musk.",
        "streaming": false
    }')

echo -e "${GREEN}📥 响应:${NC}"
echo "${RESPONSE2}" | jq -r '.result // .error // .'
echo ""
echo -e "${CYAN}⏳ 等待 2 秒后进入下一轮...${NC}"
sleep 2
echo ""

# 第3轮对话 - 测试记忆能力
echo "========================================================================"
echo -e "${BLUE}🗣️  第 3 轮对话 (测试记忆能力)${NC}"
echo "========================================================================"
echo -e "${YELLOW}📤 发送: What's my name? Can you remember it?${NC}"
echo ""

RESPONSE3=$(curl -s -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{
        "prompt": "What'\''s my name? Can you remember it?",
        "streaming": false
    }')

echo -e "${GREEN}📥 响应:${NC}"
echo "${RESPONSE3}" | jq -r '.result // .error // .'
echo ""

# 检查是否记住名字
if echo "${RESPONSE3}" | grep -qi "jason"; then
    echo -e "${GREEN}✅ 成功！Agent 记住了你的名字！${NC}"
else
    echo -e "${YELLOW}⚠️  警告：Agent 可能没有记住你的名字${NC}"
fi

echo ""
echo "========================================================================"
echo -e "${GREEN}✅ 多轮对话测试完成${NC}"
echo "========================================================================"
echo ""

