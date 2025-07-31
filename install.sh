#!/bin/bash

# 安装依赖
apt update && apt install -y python3 python3-pip git

# Clone 项目
WORKDIR=/opt/scripts/ping2wechat
mkdir -p ${WORKDIR} && cd ${WORKDIR}
# git clone https://github.com/yaf0/ping2wechat.git .

# 安装Python依赖
pip3 install -r requirements.txt

# 替换企业微信告警KEY
sed -i "s|YOUR_WECHAT_KEY|这里改为你的KEY|g" alerts.py

# 设置系统服务、自启动
cp ping2wechat.service /etc/systemd/system/
systemctl daemon-reload
systemctl start ping2wechat
systemctl enable ping2wechat

