import asyncio
import os
import json
import uuid
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
  # 创建唯一的 runtimeSessionId
  runtime_session_id = str(uuid.uuid4())
  
  print("\n" + "="*80)
  print("🔑 生成会话ID")
  print("="*80)
  print(f"Runtime Session ID: {runtime_session_id}")
  print("="*80 + "\n")
  
  # 定义多轮对话内容
  conversation_rounds = [
    "Hello, agent! My name is Jason.",
    "Tell me something about Elon Musk.",
    "What's my name? Can you remember it?"
  ]
  
  try:
    for round_num, prompt in enumerate(conversation_rounds, 1):
      print("\n" + "="*80)
      print(f"🚀 第 {round_num} 轮对话")
      print("="*80)
      
      payload = json.dumps({"prompt": prompt}).encode()
      print(f"📤 发送 Payload: {payload.decode()}")
      print(f"🎯 Agent ID: {os.getenv('PPIO_AGENT_ID')}")
      print(f"🔑 Session ID: {runtime_session_id}")
      
      response = await client.invoke_agent_runtime(
        agentId=os.getenv("PPIO_AGENT_ID"),
        payload=payload,
        timeout=300,
        envVars={"PPIO_AGENT_API_KEY": os.getenv("PPIO_AGENT_API_KEY")},
        runtimeSessionId=runtime_session_id  # 使用相同的 sessionId
      )
      
      print("\n" + "-"*80)
      print(f"✅ 第 {round_num} 轮响应")
      print("-"*80)
      print(f"Response type: {type(response)}")
      print(f"Response: {response}")
      print("-"*80)
      
      # 在下一轮对话前暂停一下
      if round_num < len(conversation_rounds):
        print("\n⏳ 等待 2 秒后进入下一轮...")
        await asyncio.sleep(2)
    
    print("\n" + "="*80)
    print("✅ 所有对话轮次完成")
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

