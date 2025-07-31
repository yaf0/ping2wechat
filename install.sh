#!/bin/bash

# 检查是否传入了企业微信机器人KEY
if [ -z "$1" ]; then
  echo "使用方法: $0 <您的企业微信机器人KEY>"
  echo "例如: $0 这里填写您的实际企业微信机器人KEY"
  exit 1
fi

WECHAT_KEY="$1"

# 安装依赖
echo "正在更新apt软件包并安装依赖..."
apt update && apt install -y python3 python3-pip git || { echo "安装依赖失败。退出。"; exit 1; }

# Clone 项目
WORKDIR=/opt/scripts/ping2wechat
echo "正在创建工作目录: ${WORKDIR} 并准备项目文件..."
mkdir -p "${WORKDIR}" && cd "${WORKDIR}" || { echo "创建或进入 ${WORKDIR} 目录失败。退出。"; exit 1; }

# 注意：这里我们不再从远程克隆，而是假设脚本与项目文件在同一目录
# 如果您希望脚本执行时也克隆，请取消注释下一行
# git clone https://github.com/yaf0/ping2wechat.git .

# 安装Python依赖
echo "正在安装Python依赖..."
pip3 install -r requirements.txt || { echo "安装Python依赖失败。退出。"; exit 1; }

# 替换企业微信告警KEY
echo "正在替换 alerts.py 中的企业微信KEY..."
sed -i "s|YOUR_WECHAT_KEY|${WECHAT_KEY}|g" alerts.py || { echo "替换企业微信KEY失败。退出。"; exit 1; }

# 设置系统服务、自启动
echo "正在设置systemd服务..."
cp ping2wechat.service /etc/systemd/system/ || { echo "复制服务文件失败。退出。"; exit 1; }
systemctl daemon-reload
systemctl start ping2wechat
systemctl enable ping2wechat

echo "ping2wechat 安装完成！服务已启动并设置为开机自启动。"
echo "使用的企业微信KEY: ${WECHAT_KEY}"
