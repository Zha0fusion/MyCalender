#!/bin/bash

# Step 1: 杀掉旧的 python http.server 进程
echo "🔪 杀掉已有的 http.server（如果有）..."
pkill -f "python3 -m http.server"

# Step 2: 启动新的 HTTP 服务在端口 8888
PORT=8888
echo "🚀 启动 HTTP 服务监听端口 $PORT ..."
nohup python3 -m http.server $PORT > server.log 2>&1 &

# Step 3: 获取本机局域网 IP 地址
IP=$(hostname -I | awk '{print $1}')
URL="http://$IP:$PORT/Grayoutput.jpg"

# Step 4: 输出图片访问地址
echo "✅ 图片访问地址：$URL"
