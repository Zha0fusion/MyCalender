#!/bin/bash

# 切换到当前脚本所在目录（确保无论从哪运行都能找到 main.py）
cd "$(dirname "$0")"

# 运行 main.py
python3 main.py

echo "Ran at $(date)" >> cronlog.txt