"""
日志配置模块
负责人：组长
作用：配置项目的日志记录系统，包括文件日志和控制台日志
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from config.settings import get_settings

settings = get_settings()


def setup_logging():
    """设置项目日志配置"""
    # 创建日志目录
    log_dir = os.path.dirname(settings.log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 获取根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # 清除现有处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        settings.log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, settings.log_level.upper()))
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("langchain").setLevel(logging.WARNING)
    
    logging.info("日志系统初始化完成")