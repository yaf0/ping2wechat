import subprocess
import logging
from alerts import send_alert
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time

PING_COUNT = 100  # 默认值，如果配置文件中没有设定
PING_INTERVAL_MS = 150
MAX_THREADS = 15

def ping_ip(ip, hostname, remark, loss_rate_threshold, latency_threshold_ms):
    try:
        result = subprocess.run(
            ['ping', '-c', str(PING_COUNT), '-W', '1', '-i', str(PING_INTERVAL_MS / 1000), ip],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output = result.stdout

        # 解析丢包率
        loss_rate = parse_loss_rate(output)
        avg_latency = parse_avg_latency(output)

        log_result(hostname, ip, remark, loss_rate, avg_latency)

        # 判断丢包率和延迟是否超过阈值，并发送告警
        if loss_rate >= loss_rate_threshold:
            send_alert(hostname, ip, f"{remark} - 丢包率: {loss_rate}%")
        if avg_latency and avg_latency > latency_threshold_ms:
            send_alert(hostname, ip, f"{remark} - 平均延迟: {avg_latency:.0f} ms")

    except Exception as e:
        logging.error(f"Error executing ping for {ip}: {e}")
        send_alert(hostname, ip, f"{remark} - IP无法访问")

def parse_loss_rate(output):
    loss_line = [line for line in output.split('\n') if 'packet loss' in line]
    if loss_line:
        loss_rate_str = loss_line[0].split(',')[2].strip().split('%')[0]
        return int(loss_rate_str)
    return 100  # 无法解析时，假设全部丢包

def parse_avg_latency(output):
    latency_line = [line for line in output.split('\n') if 'rtt min/avg/max/mdev' in line]
    if latency_line:
        return float(latency_line[0].split('/')[4].strip())
    return None

def log_result(hostname, ip, remark, loss_rate, avg_latency):
    if avg_latency is not None:
        logging.info(f'{hostname} - {ip} - {remark} - Loss rate: {loss_rate}%, Avg latency: {avg_latency:.0f} ms')
    else:
        logging.info(f'{hostname} - {ip} - {remark} - Loss rate: {loss_rate}%, Avg latency: N/A ms')

def monitor(config):
    global PING_COUNT, PING_INTERVAL_MS
    PING_COUNT = config.getint('settings', 'ping_count', fallback=100)
    PING_INTERVAL_MS = config.getint('settings', 'ping_interval_ms', fallback=150)

    while True:
        current_hour = datetime.now().hour
        if 8 <= current_hour < 22:
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                futures = []
                for section in config.sections():
                    remark = config.get(section, 'remark', fallback='')
                    if '禁用' in remark:
                        continue
                    hostname = section
                    ips = config.get(section, 'ips').split(',')

                    loss_rate_threshold = config.getint(section, 'loss_threshold', fallback=2)
                    latency_threshold_ms = config.getint(section, 'latency_threshold', fallback=100)

                    for ip in ips:
                        futures.append(executor.submit(ping_ip, ip, hostname, remark, loss_rate_threshold, latency_threshold_ms))

                for future in as_completed(futures):
                    future.result()

        # 每20秒检查一次
        time.sleep(20)

