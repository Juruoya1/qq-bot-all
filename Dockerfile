FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 下载 go-cqhttp
RUN wget https://github.com/Mrs4s/go-cqhttp/releases/download/v1.2.0/go-cqhttp_linux_amd64.tar.gz \
    && tar -xzf go-cqhttp_linux_amd64.tar.gz \
    && rm go-cqhttp_linux_amd64.tar.gz \
    && chmod +x go-cqhttp

# 设置工作目录
WORKDIR /app

# 复制 Python 依赖文件
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制所有代码
COPY . .

# 创建启动脚本
RUN echo '#!/bin/bash\n\
# 启动 go-cqhttp 在后台\n\
./go-cqhttp -c config.yml > cq.log 2>&1 &\n\
# 等待几秒让 go-cqhttp 启动\n\
sleep 5\n\
# 启动 NoneBot\n\
python bot.py' > start.sh && chmod +x start.sh

# 暴露端口
EXPOSE 6700 8080

# 启动
CMD ["./start.sh"]
