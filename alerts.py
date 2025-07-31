import requests
from datetime import datetime
import logging
from requests.exceptions import RequestException

ALARM_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WECHAT_KEY"

def send_alert(hostname, ip, message, retries=3):
    """
    发送告警消息到企业微信。

    Args:
        hostname (str): 主机名称
        ip (str): IP 地址
        message (str): 告警信息
        retries (int): 重试次数，默认为 3 次

    Returns:
        bool: 告警是否发送成功
    """
    current_time = datetime.now().strftime('%m-%d %H:%M:%S')
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"时间：{current_time}\n主机：{hostname}\nIP：{ip}\n{message}"
        }
    }

    for _ in range(retries):
        try:
            response = requests.post(ALARM_URL, json=payload, timeout=10)
            if response.status_code == 200:
                return True
        except RequestException as e:
            logging.error(f"告警发送失败: {e}")
    return False

