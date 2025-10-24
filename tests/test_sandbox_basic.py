import asyncio
import os
import json
from ppio_sandbox.agent_runtime import AgentRuntimeClient as PPIOAgentRuntimeClient
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("PPIO_API_KEY"))
print(os.getenv("PPIO_DOMAIN"))
print(os.getenv("PPIO_AGENT_ID"))
print(os.getenv("PPIO_AGENT_API_KEY"))

client = PPIOAgentRuntimeClient(
  api_key=os.getenv("PPIO_API_KEY")
)

async def main():
  try:
    print("\n" + "="*80)
    print("🚀 开始调用 Agent")
    print("="*80)
    
    payload = json.dumps({"prompt": "Hello, Agent! Tell me something about Elon Musk."}).encode()
    print(f"📤 发送 Payload: {payload.decode()}")
    print(f"🎯 Agent ID: {os.getenv('PPIO_AGENT_ID')}")
    
    response = await client.invoke_agent_runtime(
      agentId=os.getenv("PPIO_AGENT_ID"),
      payload=payload,
      timeout=300,
      envVars={"PPIO_AGENT_API_KEY": os.getenv("PPIO_AGENT_API_KEY")},
    )
    
    print("\n" + "="*80)
    print("✅ 收到响应")
    print("="*80)
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    print("="*80 + "\n")
    
  except Exception as e:
    print("\n" + "="*80)
    print("❌ 调用失败")
    print("="*80)
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {str(e)}")
    import traceback
    print("\n完整堆栈:")
    traceback.print_exc()
    print("="*80 + "\n")

if __name__ == "__main__":
  asyncio.run(main())