FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# 下载 go-cqhttp
RUN wget https://github.com/Mrs4s/go-cqhttp/releases/download/v1.2.0/go-cqhttp_linux_amd64.tar.gz \
    && tar -xzf go-cqhttp_linux_amd64.tar.gz \
    && rm go-cqhttp_linux_amd64.tar.gz \
    && chmod +x go-cqhttp

WORKDIR /app

# 复制文件
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

# 创建更健壮的启动脚本
RUN echo '#!/bin/bash\n\
echo "=================================================="\n\
echo "🚀 启动 go-cqhttp..."\n\
./go-cqhttp -c config.yml > cq.log 2>&1 &\n\
GO_PID=$!\n\
echo "go-cqhttp PID: $GO_PID"\n\
\n\
# 等待 go-cqhttp 启动\n\
echo "等待 go-cqhttp 启动..."\n\
sleep 10\n\
\n\
# 检查 go-cqhttp 是否在运行\n\
if ps -p $GO_PID > /dev/null; then\n\
    echo "✅ go-cqhttp 启动成功"\n\
    # 检查端口监听\n\
    netstat -tlnp | grep 6700\n\
else\n\
    echo "❌ go-cqhttp 启动失败"\n\
    cat cq.log\n\
fi\n\
\n\
echo "=================================================="\n\
echo "🤖 启动 NoneBot..."\n\
python bot.py' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
