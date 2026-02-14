import os
import threading
import time
import requests
import subprocess
import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置 NoneBot 使用反向 WebSocket（等待 go-cqhttp 连接）
os.environ['ONEBOT_WS_URLS'] = '[]'  # 不主动连接，等待被连接

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(OneBotV11Adapter)

# 加载插件
nonebot.load_plugins("plugins")

def check_go_cqhttp():
    """检查 go-cqhttp 状态"""
    import socket
    while True:
        time.sleep(30)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 6700))
            if result == 0:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ go-cqhttp 已连接")
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ go-cqhttp 未连接")
            sock.close()
        except Exception as e:
            print(f"检查失败: {e}")

def keep_alive():
    """保活函数"""
    url = os.environ.get('RAILWAY_URL', '')
    if not url:
        return
    
    while True:
        time.sleep(240)
        try:
            requests.get(url, timeout=5)
        except:
            pass

if __name__ == '__main__':
    print("="*50)
    print("🤖 AI QQ机器人启动中...")
    print("="*50)
    
    # 启动 go-cqhttp 检查线程
    threading.Thread(target=check_go_cqhttp, daemon=True).start()
    
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
