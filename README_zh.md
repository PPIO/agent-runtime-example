# PPIO Agent Runtime - LangGraph 示例

**使用 LangGraph 构建 AI Agent，并在几分钟内部署到 PPIO Agent Runtime。**

这个示例向你展示如何将一个包含流式响应、多轮对话和工具集成的 AI Agent 快速部署到 PPIO Agent Runtime。

[English](README.md) | 简体中文

## 📋 目录

- [示例内容](#-示例内容)
- [快速开始](#-快速开始)
  - [准备工作](#准备工作)
  - [本地运行](#本地运行)
  - [部署到 PPIO Agent Runtime](#部署到-ppio-agent-runtime)
- [项目结构](#-项目结构)
- [Agent 能力](#-Agent能力)
- [测试](#-测试)
- [API 参考](#-api-参考)
- [常见问题](#-常见问题)
- [资源链接](#-资源链接)

## ✨ 示例内容

这个 Agent 示例包含了以下能力：

- ✅ **流式响应** - 实时输出 token，提升用户体验
- ✅ **多轮对话** - 自动管理对话历史
- ✅ **工具集成** - DuckDuckGo 搜索功能
- ✅ **完整测试** - 本地和生产环境测试

## 🚀 快速开始

### 准备工作

开始之前，请安装以下环境：

- **Python 3.9+** 和 **Node.js 20+**
- **PPIO API 密钥** - [在控制台获取](https://ppio.com/settings/key-management)

### 本地运行

**1. 克隆代码仓库**

```bash
git clone git@github.com:PPIO/agent-runtime-example.git
cd agent-runtime-example
```

**2. 创建 Python 虚拟环境**

```bash
python -m venv .venv

# macOS/Linux：
source .venv/bin/activate

# Windows：
.venv\Scripts\activate
```

**3. 安装 Python 依赖**

```bash
pip install -r requirements.txt
```

**4. 在 `.env` 中添加 API 密钥**

复制示例文件并添加密钥：

```bash
cp .env.example .env
```

编辑 `.env` 填入以下必需的值：

| 变量 | 说明 | 获取位置 |
|------|------|----------|
| `PPIO_API_KEY` | PPIO 平台 API 密钥 | [PPIO 控制台 → 密钥管理](https://ppio.ai/settings/key-management) |
| `PPIO_AGENT_API_KEY` | Agent 中用来调用 LLM API 的 PPIO API 密钥 | 同上 |

**5. 在本地启动 Agent**

```bash
python app.py
```

Agent 运行在 `http://localhost:8080`。测试一下：

```bash
bash tests/test_local_basic.sh
```

你应该看到 Agent 返回的 JSON 响应。

### 部署到 PPIO Agent Runtime

**1. 验证 PPIO CLI 已安装**

```bash
npx ppio-sandbox-cli@beta --version
```

**2. 配置 Agent**

运行交互式配置（仅首次部署）：

```bash
npx ppio-sandbox-cli@beta agent configure
```

CLI 会创建三个文件：
- `.ppio-agent.yaml` - Agent 元信息和配置
- `ppio.Dockerfile` - 沙箱模板 Dockerfile
- `.dockerignore` - 排除文件列表

**3. 部署到 PPIO 云端**

```bash
npx ppio-sandbox-cli@beta agent launch
```

部署成功后，`.ppio-agent.yaml` 包含你的 Agent ID：

```yaml
status:
  phase: deployed
  agent_id: agent-xxxx  # ⭐ 调用 Agent 需要这个 ID
  last_deployed: '2025-10-23T10:35:00Z'
```

**4. 使用 CLI 测试**

调用已部署的 Agent：

```bash
npx ppio-sandbox-cli@beta agent invoke "Hello, Agent!"
```

CLI 会自动从 `.ppio-agent.yaml` 读取 `agent_id`。

**5. 在你的应用中使用 SDK 调用 Agent**

将 `.ppio-agent.yaml` 中的 Agent ID 保存到 `.env` 文件中：

```bash
PPIO_AGENT_ID=agent-xxxx  # 从 .ppio-agent.yaml 的 status.agent_id 复制
```

测试 SDK 调用：

```bash
# 非流式响应测试
python tests/test_sandbox_basic.py

# 流式响应测试
python tests/test_sandbox_streaming.py

# 多轮对话测试
python tests/test_sandbox_multi_turn.py
```

## 📁 项目结构

```
ppio-agent-example/
├── app.py                          # Agent 程序
├── tests/                          # 所有测试文件
│   ├── test_local_basic.sh         # 本地基础测试
│   ├── test_local_streaming.sh     # 本地流式响应测试
│   ├── test_local_multi_turn.sh    # 本地多轮对话测试
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

## 🏗️ Agent 能力

这个示例 Agent 具有三个主要功能：

### 💬 多轮对话

Agent 自动记住对话历史。每个沙箱实例维护自己的对话上下文。

**对话示例：**
```
第 1 轮：
用户："我叫 Alice"
Agent："很高兴认识你，Alice！"

第 2 轮（同一会话）：
用户："我叫什么名字？"
Agent："你的名字是 Alice。"
```

使用 SDK 时，传入相同的 `runtimeSessionId` 参数可以维持同一会话。

### 🌐 互联网搜索能力

Agent 可以在需要时搜索 DuckDuckGo 获取最新信息。

LangGraph 工作流自动处理：
1. Agent 判断是否需要信息
2. Agent 调用搜索工具
3. Agent 将搜索结果整合到回答中

### 📡 流式和非流式响应

每次请求可通过 `streaming` 参数选择是否返回流式数据。

## 🧪 测试

### 本地测试（开发环境）

本地测试针对运行在 `localhost:8080` 的 `app.py`。

**启动 Agent：**

```bash
python app.py
```

**在另一个终端运行测试：**

```bash
# 基础测试
bash tests/test_local_basic.sh

# 流式响应测试
bash tests/test_local_streaming.sh

# 多轮对话测试
bash tests/test_local_multi_turn.sh
```

> **Windows 用户：** 使用 Git Bash 或 WSL 运行 bash 脚本。

### 生产测试（PPIO 沙箱）

生产测试使用 SDK 调用已部署的 Agent。

**前置条件：**
- 已用 `agent launch` 命令部署 Agent
- 已在 `.env` 文件中添加 `PPIO_AGENT_ID`

**运行测试：**

```bash
# 非流式响应
python tests/test_sandbox_basic.py

# 流式响应
python tests/test_sandbox_streaming.py

# 多轮对话
python tests/test_sandbox_multi_turn.py
```

如果 Agent 配置正确，所有测试都应通过。

## 🔌 API 参考

### 健康检查端点

检查 Agent 是否正常运行：

```bash
GET /ping
```

**响应：**
```json
{
  "status": "healthy",
  "service": "My Agent"
}
```

### Agent 调用端点

向 Agent 发送请求：

```bash
POST /invocations
```

**请求体参数：**

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `prompt` | 字符串 | ✅ 是 | - | 用户消息或问题 |
| `streaming` | 布尔值 | 否 | `false` | 启用流式输出 |

**请求示例：**
```json
{
  "prompt": "告诉我关于 AI 智能体的信息",
  "streaming": false
}
```

**非流式响应：**
```json
{
  "result": "AI 智能体是能够自主..."
}
```

**流式响应：**

服务器发送事件（SSE）格式：

```
data: {"chunk": "AI ", "type": "content"}
data: {"chunk": "智能体 ", "type": "content"}
data: {"chunk": "是 ", "type": "content"}
...
data: {"chunk": "", "type": "end"}
```

每行 `data:` 包含一个带有下一个 token 的 JSON 对象。

## 🔧 常见问题

### Agent 不记得之前的消息

**原因：** 每次沙箱重启会创建新的对话历史。

**解决方法：** 在 SDK 调用中使用相同的 `runtimeSessionId` 参数来维持同一沙箱实例：

```python
response = await client.invoke_agent_runtime(
    agentId=agent_id,
    payload=payload,
    runtimeSessionId="unique-session-id",  # 多轮对话使用相同 ID
    timeout=300
)
```

### 流式输出不工作

**原因：** 可能缺少 `streaming` 参数或设置为 `false`。

**解决方法：** 确保请求中包含 `"streaming": true`：

```json
{
  "prompt": "你的问题",
  "streaming": true
}
```

### 本地运行时出现导入错误

**原因：** 依赖未安装或 Python 环境不正确。

**解决方法：** 
1. 激活虚拟环境
2. 安装依赖：`pip install -r requirements.txt`
3. 验证安装：`pip list | grep ppio-sandbox`

## 📚 资源链接

- [PPIO Agent Runtime 文档](https://ppio.com/docs/sandbox/agent-runtime-introduction)
- [PPIO Agent 沙箱文档](https://ppio.com/docs/sandbox/overview)

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

**需要帮助？** 提交 issue 或访问 [ppio.ai](https://ppio.ai) 联系支持。

