# PPIO Agent Runtime - LangGraph 示例

一个完整的示例项目，展示如何将 LangGraph 智能体集成到 PPIO Agent Runtime 平台，支持流式响应和带简单记忆的多轮对话。

[English](README.md) | 简体中文

## 🎯 概述

本项目展示了一个生产就绪的 AI 智能体，使用：
- **LangGraph** 进行智能体编排和状态管理
- **LangChain** 进行 LLM 集成和工具调用
- **PPIO Agent Runtime** 进行部署和扩展
- **DuckDuckGo 搜索** 作为示例工具

该智能体支持流式和非流式响应，并在沙箱生命周期内保持对话上下文，实现自然的多轮交互。

## ✨ 特性

- ✅ **LangGraph 集成**，支持工具调用
- ✅ **流式和非流式**响应支持
- ✅ **多轮对话**，带简单记忆
- ✅ **DuckDuckGo 搜索**集成
- ✅ **完整的测试**套件
- ✅ **生产就绪**的日志和错误处理

## 🚀 快速开始

### 前置要求

- Python 3.12+
- PPIO 平台账号 ([在这里注册](https://ppio.ai))
- 你选择的 LLM 提供商的 API 密钥

### 安装

1. 克隆此仓库：
```bash
git clone <your-repo-url>
cd ppio-agent-example
```

2. 创建并激活虚拟环境（推荐）：
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 使用你的实际凭据编辑 .env
```

`.env` 中需要的环境变量：
```bash
# PPIO 平台配置
PPIO_API_KEY=your_api_key_here
PPIO_DOMAIN=your_domain_here
PPIO_AGENT_ID=your_agent_id_here
PPIO_AGENT_API_KEY=your_agent_api_key_here
```

### 本地运行

本地启动智能体进行开发和测试：
```bash
python app.py
```

智能体将在 `http://localhost:8080` 上启动。

### 部署到 PPIO 平台

将智能体部署到 PPIO 沙箱环境：

1. **安装 PPIO CLI**（如果尚未安装）：
```bash
npx ppio-sandbox-cli@beta --version
```

2. **配置 Agent**（首次部署时）：
```bash
npx ppio-sandbox-cli@beta agent configure
```
这将交互式地引导你配置 Agent，并生成以下文件：
- `.ppio-agent.yaml` - Agent 配置文件
- `ppio.Dockerfile` - Docker 构建文件
- `.dockerignore` - Docker 忽略文件

3. **部署 Agent**：
```bash
npx ppio-sandbox-cli@beta agent launch
```

部署成功后，Agent ID 会保存在 `.ppio-agent.yaml` 的 `status.agent_id` 字段：
```yaml
status:
  phase: deployed
  agent_id: agent-xxxx  # ⭐ Agent 的唯一标识
  last_deployed: '2025-10-23T10:35:00Z'
```

4. **快速测试**（使用 CLI）：
```bash
# CLI 会自动从 .ppio-agent.yaml 读取 agent_id
npx ppio-sandbox-cli@beta agent invoke "Hello, Agent!"
```

5. **使用 SDK 调用**（生产环境推荐）：

在 `.env` 文件中配置 Agent ID：
```bash
PPIO_AGENT_ID=agent-xxxx  # 从 .ppio-agent.yaml 的 status.agent_id 获取
```

使用提供的测试脚本：
```bash
# 基础测试（非流式响应，单轮对话）
python tests/test_sandbox_basic.py

# 流式测试（流式响应，单轮对话）
python tests/test_sandbox_streaming.py

# 多轮对话测试（非流式响应，多轮对话）
python tests/test_sandbox_multi_turn.py
```

这些脚本使用 `ppio_sandbox.agent_runtime.AgentRuntimeClient` 来调用已部署的 agent：

```python
from ppio_sandbox.agent_runtime import AgentRuntimeClient

client = AgentRuntimeClient(api_key=os.getenv("PPIO_API_KEY"))

# 调用 agent
response = await client.invoke_agent_runtime(
    agentId=os.getenv("PPIO_AGENT_ID"),
    payload=json.dumps({"prompt": "Hello!"}).encode(),
    timeout=300,
    envVars={
        "PPIO_AGENT_API_KEY": os.getenv("PPIO_API_KEY"),
        # 其他需要传递到沙箱的环境变量
    }
)
```


## 📁 项目结构

```
ppio-agent-example/
├── app.py                          # 主智能体应用程序
├── tests/                          # 所有测试文件
│   ├── test_local_basic.sh         # 本地基础测试（非流式）
│   ├── test_local_streaming.sh     # 本地流式测试（单轮）
│   ├── test_local_multi_turn.sh    # 本地多轮测试（非流式）
│   ├── test_sandbox_basic.py       # 远程基础测试
│   ├── test_sandbox_streaming.py   # 远程流式测试
│   └── test_sandbox_multi_turn.py  # 远程多轮测试
├── app_logs/                       # 应用程序日志（运行时生成）
├── .env.example                    # 环境变量模板
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
├── README_zh.md
└── LICENSE
```

## 🏗️ 架构

### Agent 功能

这是一个基于 LangGraph 构建的示例 AI Agent，展示了如何集成到 PPIO 平台。它具备以下能力：

1. **💬 对话能力**
   - 支持单轮和多轮对话
   - 自动维护对话历史（在沙箱生命周期内）

2. **🌐 工具调用**
   - 集成了 DuckDuckGo 搜索工具
   - 可以实时搜索互联网信息

3. **📡 灵活响应**
   - 支持流式响应
   - 请求时动态选择响应模式

## 🧪 测试

### 本地测试（HTTP）

针对运行在 `localhost:8080` 的 `app.py` 运行本地测试：

```bash
# 1. 在一个终端启动智能体
python app.py

# 2. 在另一个终端运行测试：

# 基础测试（非流式响应，单轮对话）
bash tests/test_local_basic.sh

# 流式测试（流式响应，单轮对话）
bash tests/test_local_streaming.sh

# 多轮对话测试（非流式响应，多轮对话）
bash tests/test_local_multi_turn.sh
```

**注意：** Shell 脚本需要 bash 环境（macOS/Linux 自带）。Windows 用户可以使用 Git Bash 或 WSL。

### 远程测试（沙箱）

在 PPIO 沙箱环境中测试已部署的智能体：

```bash
# 基础测试（非流式响应，单轮对话）
python tests/test_sandbox_basic.py

# 流式测试（流式响应，单轮对话）
python tests/test_sandbox_streaming.py

# 多轮对话测试（非流式响应，多轮对话）
python tests/test_sandbox_multi_turn.py
```

运行远程测试前，请确保已在 `.env` 中配置了你的 PPIO 凭据。

## 🔌 API 参考

### GET /ping

健康检查端点。

**响应：**
```json
{
  "status": "healthy",
  "service": "My Agent"
}
```

### POST /invocations

主智能体调用端点。

**请求：**
```json
{
  "prompt": "告诉我关于 AI 智能体的信息",
  "streaming": false
}
```

**参数：**
- `prompt`（字符串，必需）：用户的消息/问题
- `streaming`（布尔值，可选）：启用流式响应，默认为 `false`

**响应（非流式）：**
```json
{
  "result": "AI 智能体是自主系统..."
}
```

**响应（流式）：**
服务器发送事件（SSE）格式：
```
data: {"chunk": "AI ", "type": "content"}
data: {"chunk": "智能体 ", "type": "content"}
data: {"chunk": "是 ", "type": "content"}
...
data: {"chunk": "", "type": "end"}
```

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 📚 资源

- [PPIO Agent Runtime 文档]()

