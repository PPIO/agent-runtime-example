import asyncio
import os
import json
import time
import sys
from ppio_sandbox.agent_runtime import AgentRuntimeClient as PPIOAgentRuntimeClient
from dotenv import load_dotenv
load_dotenv()

# 强制禁用 stdout 缓冲，确保实时输出
sys.stdout.reconfigure(line_buffering=True)

# 调试模式：显示每个 chunk 的详细信息和时间戳
DEBUG_MODE = True  # 先启用调试模式，看看 chunk 是否实时到达

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
    print("🚀 开始调用 Agent（流式模式）")
    print("="*80)
    
    # 使用 PPIO 标准字段 'stream'（不是 'streaming'）
    request_dict = {"prompt": "Hello, Agent! Tell me something about Elon Musk.", "streaming": True}
    payload = json.dumps(request_dict).encode()
    print(f"📤 发送 Payload: {json.dumps(request_dict, ensure_ascii=False)}")
    print(f"🎯 Agent ID: {os.getenv('PPIO_AGENT_ID')}")
    
    # 使用标准的 SDK 方法
    print("\n⏱️  调用 invoke_agent_runtime，等待首个响应...")
    invoke_start_time = time.time()
    
    response = await client.invoke_agent_runtime(
      agentId=os.getenv("PPIO_AGENT_ID"),
      payload=payload,
      timeout=300,
      envVars={"PPIO_AGENT_API_KEY": os.getenv("PPIO_AGENT_API_KEY")},
    )
    
    first_response_time = time.time() - invoke_start_time
    print(f"✅ 收到响应对象，耗时: {first_response_time:.3f}秒")
    
    print("\n" + "="*80)
    print("📡 开始接收数据...")
    print("="*80 + "\n")
    
    # 检查响应类型
    print(f"Response type: {type(response)}")
    print(f"Has __aiter__: {hasattr(response, '__aiter__')}")
    
    # 处理流式响应
    if hasattr(response, '__aiter__'):
      # 如果是异步迭代器（流式响应）
      print("\n💬 Agent 回复（流式）:\n")
      print("-" * 80)
      chunk_count = 0
      content_count = 0
      
      start_time = time.time()
      last_chunk_time = start_time
      
      print(f"⏱️  开始迭代响应流，当前时间戳: {time.time():.3f}")
      iteration_start = time.time()
      
      async for chunk in response:
        chunk_count += 1
        current_time = time.time()
        time_since_start = current_time - start_time
        time_since_last = current_time - last_chunk_time
        last_chunk_time = current_time
        
        # 第一个 chunk 到达的特殊日志
        if chunk_count == 1:
          time_to_first_chunk = current_time - iteration_start
          sys.stdout.write(f"\n🎉 第一个 chunk 到达！从开始迭代到现在: {time_to_first_chunk:.3f}秒\n")
          sys.stdout.write(f"   从 invoke 调用到现在总耗时: {current_time - invoke_start_time:.3f}秒\n\n")
          sys.stdout.flush()
        
        if DEBUG_MODE:
          # 使用 sys.stdout.write 和立即 flush 确保实时输出
          debug_msg = f"\n[Chunk #{chunk_count}] +{time_since_last:.3f}s | Type: {type(chunk).__name__}\n"
          sys.stdout.write(debug_msg)
          sys.stdout.flush()
        
        # 解析 chunk 的辅助函数
        def parse_and_print(data):
          nonlocal content_count
          if isinstance(data, dict):
            if data.get('type') == 'content':
              content = data.get('chunk', '')
              if content:
                content_count += 1
                # 使用 sys.stdout.write 代替 print，确保实时输出
                sys.stdout.write(content)
                sys.stdout.flush()
                
                if DEBUG_MODE:
                  sys.stdout.write(f" [{len(content)} chars]")
                  sys.stdout.flush()
            elif data.get('type') == 'end':
              sys.stdout.write(f"\n{'-' * 80}\n")
              sys.stdout.write(f"✅ 流式传输完成\n")
              sys.stdout.write(f"   总数据块: {chunk_count}\n")
              sys.stdout.write(f"   内容块: {content_count}\n")
              sys.stdout.write(f"   总耗时: {time_since_start:.2f}秒\n")
              sys.stdout.flush()
            elif data.get('type') == 'error':
              sys.stdout.write(f"\n❌ 错误: {data.get('error')}\n")
              sys.stdout.flush()
          else:
            sys.stdout.write(str(data))
            sys.stdout.flush()
        
        # 处理不同格式的 chunk
        if isinstance(chunk, str):
          # 字符串格式：可能是 JSON 字符串
          try:
            data = json.loads(chunk)
            parse_and_print(data)
          except json.JSONDecodeError:
            # 不是 JSON，直接输出
            sys.stdout.write(chunk)
            sys.stdout.flush()
        
        elif isinstance(chunk, dict):
          # 字典格式：可能直接是数据，或者包含嵌套的 'chunk' 键
          if 'chunk' in chunk and isinstance(chunk['chunk'], str):
            # SDK 包装格式：{'chunk': '...', ...}
            try:
              inner_data = json.loads(chunk['chunk'])
              parse_and_print(inner_data)
            except (json.JSONDecodeError, TypeError):
              # 不是 JSON，直接输出
              sys.stdout.write(chunk['chunk'])
              sys.stdout.flush()
          else:
            # 直接是数据格式
            parse_and_print(chunk)
        
        else:
          # 其他类型，直接输出
          sys.stdout.write(str(chunk))
          sys.stdout.flush()
      
      if chunk_count == 0:
        print("⚠️ 没有收到任何数据块")
        
    elif isinstance(response, dict):
      # 如果是普通响应（非流式）
      print("\n💬 Agent 回复（非流式）:")
      print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
      # 其他类型
      print("\n💬 Agent 回复（未知格式）:")
      print(response)
    
    print("\n" + "="*80 + "\n")
    
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