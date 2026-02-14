from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent
import aiohttp
import os

ai = on_message()

@ai.handle()
async def handle_ai(event: MessageEvent):
    msg = event.get_plaintext().strip()
    
    if not msg.startswith('#'):
        return
    
    question = msg[1:].strip()
    if not question:
        await ai.finish("❌ 你想问什么？")
        return
    
    await ai.send("🤔 思考中...")
    
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        await ai.finish("❌ 未配置 DeepSeek API Key")
        return
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'deepseek-chat',
                    'messages': [
                        {"role": "system", "content": "你是一个友好的QQ机器人，回答简洁有趣。"},
                        {"role": "user", "content": question}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 1000
                },
                timeout=30
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    answer = data['choices'][0]['message']['content']
                    await ai.finish(f"🤖 {answer}")
                else:
                    error = await resp.text()
                    await ai.finish(f"❌ API错误: {resp.status}")
    except Exception as e:
        await ai.finish(f"❌ 请求失败: {str(e)}")
