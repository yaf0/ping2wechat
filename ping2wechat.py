import logging
from config import load_config
from ping_utils import monitor
import os

# 设置日志
from logging.handlers import RotatingFileHandler
log_handler = RotatingFileHandler('ping.log', maxBytes=5*1024*1024, backupCount=3)  # 最大5MB，备份3个文件
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    # 加载配置文件并进行检查
    config_path = 'config.ini'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件 {config_path} 不存在，请检查路径。")
    
    config = load_config(config_path)
    if not config.sections():
        raise ValueError("配置文件无效或内容为空，请检查配置文件。")

    # 开始监控
    monitor(config)

