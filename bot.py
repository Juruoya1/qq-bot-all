import os
import threading
import time
import requests
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置 NoneBot 连接本地的 go-cqhttp
os.environ['ONEBOT_WS_URLS'] = '["ws://localhost:6700"]'

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件
nonebot.load_plugins("plugins")

def keep_alive():
    """保活函数"""
    url = os.environ.get('RAILWAY_URL', '')
    if not url:
        return
    
    while True:
        time.sleep(240)
        try:
            requests.get(url, timeout=5)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 心跳正常")
        except:
            pass

def check_go_cqhttp():
    """检查 go-cqhttp 是否运行"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 6700))
    if result == 0:
        print("✅ go-cqhttp 已连接")
    else:
        print("❌ go-cqhttp 未连接")
    sock.close()

if __name__ == '__main__':
    print("="*50)
    print("🤖 AI QQ机器人启动中...")
    print("="*50)
    
    # 检查 go-cqhttp
    check_go_cqhttp()
    
    # 启动保活线程
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # 检查环境变量
    if os.environ.get('DEEPSEEK_API_KEY'):
        print("✅ DeepSeek API Key 已配置")
    else:
        print("❌ 未配置 DeepSeek API Key")
    
    print("📝 使用 # 触发AI对话")
    print("="*50)
    
    # 运行 NoneBot
    nonebot.run()
