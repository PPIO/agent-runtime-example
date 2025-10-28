# PPIO Agent Runtime - LangGraph Example

**Build AI agents with LangGraph and deploy to PPIO Agent Runtime in minutes.**

This example shows you how to quickly deploy an AI agent with streaming responses, multi-turn conversations, and tool integration to PPIO Agent Runtime.

[简体中文](README_zh.md) | English

## 📋 Table of Contents

- [What This Example Includes](#-what-this-example-includes)
- [Quick Start](#-quick-start)
  - [What You Need](#what-you-need)
  - [Run Locally](#run-locally)
  - [Deploy to PPIO Agent Runtime](#deploy-to-ppio-agent-runtime)
- [Project Structure](#-project-structure)
- [Agent Capabilities](#-agent-capabilities)
- [Testing](#-testing)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Resources](#-resources)

## ✨ What This Example Includes

This agent example includes the following capabilities:

- ✅ **Streaming responses** - Real-time token streaming for better UX
- ✅ **Multi-turn conversations** - Automatic conversation history management
- ✅ **Tool integration** - DuckDuckGo search capability
- ✅ **Complete test suite** - Both local and production tests

## 🚀 Quick Start

### What You Need

Before starting, install these requirements:

- **Python 3.9+** and **Node.js 20+**
- **PPIO API Key** - [Get it from console](https://ppio.com/settings/key-management)

### Run Locally

**1. Clone the repository**

```bash
git clone git@github.com:PPIO/agent-runtime-example.git
cd agent-runtime-example
```

**2. Create a Python virtual environment**

```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your API keys to `.env`**

Copy the example file and add your keys:

```bash
cp .env.example .env
```

Edit `.env` with these required values:

| Variable | Description | Where to Find It |
|----------|-------------|------------------|
| `PPIO_API_KEY` | Your PPIO platform API key | [PPIO Dashboard → Key Management](https://ppio.ai/settings/key-management) |
| `PPIO_AGENT_API_KEY` | PPIO API key for LLM API calls in agent | Same dashboard |

**5. Start the agent locally**

```bash
python app.py
```

The agent runs at `http://localhost:8080`. Test it:

```bash
bash tests/test_local_basic.sh
```

You should see a JSON response with the agent's answer.

### Deploy to PPIO Agent Runtime

**1. Verify PPIO CLI is installed**

```bash
npx ppio-sandbox-cli@beta --version
```

**2. Configure your agent**

Run the interactive configuration (first deployment only):

```bash
npx ppio-sandbox-cli@beta agent configure
```

The CLI creates three files:
- `.ppio-agent.yaml` - Agent metadata and configuration
- `ppio.Dockerfile` - Sandbox template Dockerfile
- `.dockerignore` - Files to exclude from Docker build

**3. Deploy to PPIO cloud**

```bash
npx ppio-sandbox-cli@beta agent launch
```

After deployment succeeds, `.ppio-agent.yaml` contains your agent ID:

```yaml
status:
  phase: deployed
  agent_id: agent-xxxx  # ⭐ You need this ID to invoke the agent
  last_deployed: '2025-10-23T10:35:00Z'
```

**4. Test with CLI**

Invoke your deployed agent:

```bash
npx ppio-sandbox-cli@beta agent invoke "Hello, Agent!"
```

The CLI reads `agent_id` automatically from `.ppio-agent.yaml`.

**5. Invoke the agent from your application with SDK**

Save the Agent ID from `.ppio-agent.yaml` to `.env` file:

```bash
PPIO_AGENT_ID=agent-xxxx  # Copy from .ppio-agent.yaml status.agent_id
```

Test SDK invocation:

```bash
# Non-streaming response test
python tests/test_sandbox_basic.py

# Streaming response test
python tests/test_sandbox_streaming.py

# Multi-turn conversation test
python tests/test_sandbox_multi_turn.py
```

## 📁 Project Structure

```
ppio-agent-example/
├── app.py                          # Agent program
├── tests/                          # All test files
│   ├── test_local_basic.sh         # Local basic test
│   ├── test_local_streaming.sh     # Local streaming response test
│   ├── test_local_multi_turn.sh    # Local multi-turn conversation test
│   ├── test_sandbox_basic.py       # Remote basic test
│   ├── test_sandbox_streaming.py   # Remote streaming test
│   └── test_sandbox_multi_turn.py  # Remote multi-turn test
├── app_logs/                       # Application logs (generated at runtime)
├── .env.example                    # Environment variable template
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
├── README_zh.md
└── LICENSE
```

## 🏗️ Agent Capabilities

This example agent has three main features:

### 💬 Multi-turn conversations

The agent remembers conversation history automatically. Each sandbox instance maintains its own conversation context.

**Example conversation:**
```
Turn 1:
User: "My name is Alice"
Agent: "Nice to meet you, Alice!"

Turn 2 (same session):
User: "What's my name?"
Agent: "Your name is Alice."
```

To maintain the same session when using the SDK, pass the same `runtimeSessionId` value across requests.

### 🌐 Internet search capability

The agent can search DuckDuckGo when it needs current information.

The LangGraph workflow handles this automatically:
1. Agent detects when information is needed
2. Agent calls the search tool
3. Agent incorporates search results into the response

### 📡 Streaming and non-streaming responses

Each request can choose whether to return streaming data via the `streaming` parameter.

## 🧪 Testing

### Local testing (development)

Local tests run against `app.py` on `localhost:8080`.

**Start the agent:**

```bash
python app.py
```

**Run tests in another terminal:**

```bash
# Basic test
bash tests/test_local_basic.sh

# Streaming response test
bash tests/test_local_streaming.sh

# Multi-turn conversation test
bash tests/test_local_multi_turn.sh
```

> **Windows users:** Use Git Bash or WSL to run bash scripts.

### Production testing (PPIO sandbox)

Production tests invoke the deployed agent using the SDK.

**Requirements:**
- Agent deployed with `agent launch` command
- `PPIO_AGENT_ID` added to `.env` file

**Run tests:**

```bash
# Non-streaming response
python tests/test_sandbox_basic.py

# Streaming response
python tests/test_sandbox_streaming.py

# Multi-turn conversation
python tests/test_sandbox_multi_turn.py
```

All tests should pass if the agent is configured correctly.

## 🔌 API Reference

### Health check endpoint

Check if the agent is running properly:

```bash
GET /ping
```

**Response:**
```json
{
  "status": "healthy",
  "service": "My Agent"
}
```

### Agent invocation endpoint

Send a request to the agent:

```bash
POST /invocations
```

**Request body parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ Yes | - | User message or question |
| `streaming` | boolean | No | `false` | Enable streaming output |

**Example request:**
```json
{
  "prompt": "Tell me about AI agents",
  "streaming": false
}
```

**Non-streaming response:**
```json
{
  "result": "AI agents are autonomous systems that..."
}
```

**Streaming response:**

Server-Sent Events (SSE) format:

```
data: {"chunk": "AI ", "type": "content"}
data: {"chunk": "agents ", "type": "content"}
data: {"chunk": "are ", "type": "content"}
...
data: {"chunk": "", "type": "end"}
```

Each `data:` line contains a JSON object with the next token chunk.

## 🔧 Troubleshooting

### Agent doesn't remember previous messages

**Cause:** Each sandbox restart creates a new conversation history.

**Solution:** Use the same `runtimeSessionId` parameter in SDK calls to maintain the same sandbox instance:

```python
response = await client.invoke_agent_runtime(
    agentId=agent_id,
    payload=payload,
    runtimeSessionId="unique-session-id",  # Same ID for multi-turn
    timeout=300
)
```

### Streaming doesn't work

**Cause:** The `streaming` parameter might be missing or set to `false`.

**Solution:** Ensure your request includes `"streaming": true`:

```json
{
  "prompt": "Your question",
  "streaming": true
}
```

### Import errors when running locally

**Cause:** Dependencies not installed or wrong Python environment.

**Solution:** 
1. Activate your virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Verify installation: `pip list | grep ppio-sandbox`

## 📚 Resources

- [PPIO Agent Runtime Documentation](https://ppio.com/docs/sandbox/agent-runtime-introduction)
- [PPIO Agent Sandbox Documentation](https://ppio.com/docs/sandbox/overview)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Need help?** Open an issue or contact support at [ppio.ai](https://ppio.ai)