# PPIO Agent Runtime - LangGraph Example

A complete example demonstrating how to integrate LangGraph agents with PPIO Agent Runtime platform, featuring streaming responses and multi-turn conversation with simple memory.

## 🎯 Overview

This project showcases a production-ready AI agent built with:
- **LangGraph** for agent orchestration and state management
- **LangChain** for LLM integration and tool calling
- **PPIO Agent Runtime** for deployment and scaling
- **DuckDuckGo Search** as an example tool

The agent supports both streaming and non-streaming responses, and maintains conversation context throughout the sandbox lifecycle for natural multi-turn interactions.

## ✨ Features

- ✅ **LangGraph integration** with tool calling
- ✅ **Streaming & non-streaming** response support
- ✅ **Multi-turn conversation** with simple memory
- ✅ **DuckDuckGo search** integration
- ✅ **Comprehensive testing** suite
- ✅ **Production-ready** logging and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PPIO Platform account ([Sign up here](https://ppio.ai))
- API keys for your chosen LLM provider

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd ppio-agent-example
```

2. Create and activate a virtual environment (recommended):
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

Required environment variables in `.env`:
```bash
# PPIO Platform Configuration
PPIO_API_KEY=your_api_key_here
PPIO_DOMAIN=your_domain_here
PPIO_AGENT_ID=your_agent_id_here
PPIO_AGENT_API_KEY=your_agent_api_key_here
```

### Local Running

Start the agent locally for development and testing:
```bash
python app.py
```

The agent will start on `http://localhost:8080`.

### Deploy to PPIO Platform

Deploy your agent to the PPIO sandbox environment:

1. **Install PPIO CLI** (if not already installed):
```bash
npx ppio-sandbox-cli@beta --version
```

2. **Configure Agent** (first-time deployment):
```bash
npx ppio-sandbox-cli@beta agent configure
```
This will guide you through an interactive configuration and generate:
- `.ppio-agent.yaml` - Agent configuration file
- `ppio.Dockerfile` - Docker build file
- `.dockerignore` - Docker ignore file

3. **Deploy Agent**:
```bash
npx ppio-sandbox-cli@beta agent launch
```

After successful deployment, the Agent ID is saved in `.ppio-agent.yaml` under `status.agent_id`:
```yaml
status:
  phase: deployed
  agent_id: agent-xxxx  # ⭐ Unique identifier for your agent
  last_deployed: '2025-10-23T10:35:00Z'
```

4. **Quick Test** (using CLI):
```bash
# CLI automatically reads agent_id from .ppio-agent.yaml
npx ppio-sandbox-cli@beta agent invoke "Hello, Agent!"
```

5. **Invoke with SDK** (recommended for production):

Configure Agent ID in `.env` file:
```bash
PPIO_AGENT_ID=agent-xxxx  # Get from .ppio-agent.yaml status.agent_id
```

Use the provided test scripts:
```bash
# Basic test (non-streaming response, single-turn)
python tests/test_sandbox_basic.py

# Streaming test (streaming response, single-turn)
python tests/test_sandbox_streaming.py

# Multi-turn test (non-streaming response, multi-turn)
python tests/test_sandbox_multi_turn.py
```

These scripts use `ppio_sandbox.agent_runtime.AgentRuntimeClient` to invoke the deployed agent:

```python
from ppio_sandbox.agent_runtime import AgentRuntimeClient

client = AgentRuntimeClient(api_key=os.getenv("PPIO_API_KEY"))

# Invoke the agent
response = await client.invoke_agent_runtime(
    agentId=os.getenv("PPIO_AGENT_ID"),
    payload=json.dumps({"prompt": "Hello!"}).encode(),
    timeout=300,
    envVars={
        "PPIO_AGENT_API_KEY": os.getenv("PPIO_API_KEY"),
        # Other environment variables to pass to sandbox
    }
)
```

## 📁 Project Structure

```
ppio-agent-example/
├── app.py                          # Main agent application
├── tests/                          # All test files
│   ├── test_local_basic.sh         # Local basic test (non-streaming)
│   ├── test_local_streaming.sh     # Local streaming test (single-turn)
│   ├── test_local_multi_turn.sh    # Local multi-turn test (non-streaming)
│   ├── test_sandbox_basic.py       # Remote basic test
│   ├── test_sandbox_streaming.py   # Remote streaming test
│   └── test_sandbox_multi_turn.py  # Remote multi-turn test
├── app_logs/                       # Application logs (generated at runtime)
├── .env.example                    # Environment variable template
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── README.md
└── LICENSE
```

## 🏗️ Architecture

### Agent Capabilities

This is a sample AI Agent built with LangGraph, demonstrating integration with the PPIO platform. It provides the following capabilities:

1. **💬 Conversation**
   - Supports single-turn and multi-turn conversations
   - Automatically maintains conversation history (during sandbox lifecycle)

2. **🌐 Tool Calling**
   - Integrated with DuckDuckGo search tool
   - Can search the internet in real-time

3. **📡 Flexible Response**
   - Supports streaming responses
   - Dynamically choose response mode per request

## 🧪 Testing

### Local Testing (HTTP)

Run local tests against `app.py` running on `localhost:8080`:

```bash
# 1. Start the agent in one terminal
python app.py

# 2. In another terminal, run tests:

# Basic test (non-streaming, single-turn)
bash tests/test_local_basic.sh

# Streaming test (single-turn)
bash tests/test_local_streaming.sh

# Multi-turn conversation test (non-streaming)
bash tests/test_local_multi_turn.sh
```

**Note:** Shell scripts require bash (available on macOS/Linux). Windows users can use Git Bash or WSL.

### Remote Testing (Sandbox)

Test deployed agent in PPIO sandbox environment:

```bash
# Basic test (non-streaming)
python tests/test_sandbox_basic.py

# Streaming test
python tests/test_sandbox_streaming.py

# Multi-turn conversation test
python tests/test_sandbox_multi_turn.py
```

Make sure you have configured your PPIO credentials in `.env` before running remote tests.

## 🔌 API Reference

### GET /ping

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "My Agent"
}
```

### POST /invocations

Main agent invocation endpoint.

**Request:**
```json
{
  "prompt": "Tell me about AI agents",
  "streaming": false
}
```

**Parameters:**
- `prompt` (string, required): User's message/question
- `streaming` (boolean, optional): Enable streaming response, default is `false`

**Response (non-streaming):**
```json
{
  "result": "AI agents are autonomous systems..."
}
```

**Response (streaming):**
Server-Sent Events (SSE) format:
```
data: {"chunk": "AI ", "type": "content"}
data: {"chunk": "agents ", "type": "content"}
data: {"chunk": "are ", "type": "content"}
...
data: {"chunk": "", "type": "end"}
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📚 Resources

- [PPIO Agent Runtime docs]()